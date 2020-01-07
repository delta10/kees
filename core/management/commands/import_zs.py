# pylint: skip-file
import re
import os
from django.core.files import File
from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import models as dest
from core.management.commands.lib import models as src

case_type_mapping = {
    7: dest.CaseType.objects.get(id=1),
    8: dest.CaseType.objects.get(id=1),
}

case_phase_mapping = {
    'Registreren': dest.Phase.objects.get(name='Registreren'),
    'Inplannen': dest.Phase.objects.get(name='Inplannen'),
    'Coordineren': dest.Phase.objects.get(name='Coördineren'),
    'Uitvoeren': dest.Phase.objects.get(name='Uitvoeren'),
    'Afhandelen': dest.Phase.objects.get(name='Afhandelen'),
}

class Command(BaseCommand):
    help = 'Import data from zs'

    def add_arguments(self, parser):
        parser.add_argument('--database-url', type=str,
                            help='The URL of the database to import from')
        parser.add_argument('--storage-path', type=str,
                            help='The path where the storage resides',
                            default='/var/tmp/zs/storage')

    def handle(self, database_url, storage_path, *args, **kwargs):
        engine = create_engine(database_url, pool_recycle=3600)
        session = sessionmaker(bind=engine)()

        for user in session.query(src.UserEntity).join(src.Subject).all():
            dest.User.objects.update_or_create(
                pk=user.id,
                defaults={
                    'username': user.subject.username,
                    'initials': user.subject.properties['initials'][:10],
                    'first_name': user.subject.properties['givenname'],
                    'last_name': user.subject.properties['sn'],
                    'password': user.password.replace('{SSHA}', 'ldap_salted_sha1$'),
                    'email': user.subject.properties['mail'],
                    'phone': user.subject.properties.get('telephonenumber')
                }
            )

        for zaak in session.query(src.Zaak).all():
            try:
                case_type = case_type_mapping[zaak.zaaktype_id]
                src_data = session.query(src.ObjectData).filter_by(object_class='case', object_id=zaak.id).first()

                if not src_data:
                    continue

                dest_data = {}
                for key, content in src_data.properties['values'].items():
                    if key.startswith('attribute.'):
                        if type(content['value']) == dict:
                            if content['value'].get('__DateTime__'):
                                value = content['value']['__DateTime__']
                            else:
                                value = content['value']
                        else:
                            value = content['value']

                        dest_data[key[10:]] = value
                    if key == 'case.phase':
                        current_phase = case_phase_mapping.get(content['value'], None)
                    if key == 'case.assignee.id':
                        try:
                            assignee = dest.User.objects.get(id=content['value'])
                        except dest.User.DoesNotExist:
                            assignee = None

                case, _ = dest.Case.objects.update_or_create(
                    pk=zaak.id,
                    defaults={
                        'case_type': case_type,
                        'current_phase': current_phase,
                        'assignee': assignee,
                        'created_at': zaak.created,
                        'data': dest_data,
                    }
                )

                for log_record in session.query(src.Logging).filter_by(zaak_id=zaak.id).all():
                    regex_result = re.findall(r'betrokkene-medewerker-(\d+)', log_record.created_by)
                    if regex_result:
                        performer = dest.User.objects.get(id=int(regex_result[0]))
                    else:
                        performer = None

                    if log_record.event_type == 'case/update/milestone':
                        case.logs.update_or_create(
                            pk=log_record.id,
                            defaults={
                                'event': 'change_phase',
                                'metadata': {
                                    'old_phase': None,
                                    'new_phase': str(case.current_phase) if case.current_phase else None,
                                },
                                'created_at': log_record.created,
                                'performer': performer
                            }
                        )
                    elif log_record.event_type == 'email/send':
                        case.logs.update_or_create(
                            pk=log_record.id,
                            defaults={
                                'event': 'send_email',
                                'metadata': {
                                    'message': 'Sucessfully sent email to {} with subject {} and message {}'.format(
                                        log_record.event_data['recipient'],
                                        log_record.event_data['subject'],
                                        log_record.event_data['content']
                                    )
                                },
                                'created_at': log_record.created,
                                'performer': performer
                            }
                        )
                    elif log_record.event_type == 'case/accept':
                        case.logs.update_or_create(
                            pk=log_record.id,
                            defaults={
                                'event': 'claim_case',
                                'created_at': log_record.created,
                                'performer': performer
                            }
                        )
                    elif log_record.event_type == 'case/note/create':
                        case.logs.update_or_create(
                            pk=log_record.id,
                            defaults={
                                'event': 'http_request',
                                'created_at': log_record.created,
                                'metadata': {
                                    'message': log_record.event_data['content'],
                                },
                                'performer': performer
                            }
                        )

                for file in session.query(src.File).filter_by(case_id=zaak.id).join(src.Filestore).all():
                    file_path = os.path.join(
                        storage_path,
                        file.filestore.uuid[0],
                        file.filestore.uuid[1],
                        file.filestore.uuid[2],
                        file.filestore.uuid[3],
                        file.filestore.uuid[4],
                        'zs_{}'.format(file.filestore.uuid)
                    )

                    try:
                        with open(file_path, 'rb') as local_file:
                            case.attachments.update_or_create(
                                pk=file.id,
                                defaults={
                                    'name': file.filestore.original_name,
                                    'file': File(local_file, name=file.filestore.original_name),
                                    'created_at': file.date_created
                                }
                            )
                    except FileNotFoundError:
                        self.stdout.write('Could not find file {}'.format(file_path))

            except KeyError:
                pass
                #self.stdout.write(
                #   'Could not map case type for case {}'.format(zaak.id))

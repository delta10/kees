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

DEST_CASE_TYPE = dest.CaseType.objects.get(id=1)

CASE_PHASE_MAPPING = {
    'Registreren': dest.Phase.objects.get(name='Registreren'),
    'Inplannen': dest.Phase.objects.get(name='Inplannen'),
    'Coordineren': dest.Phase.objects.get(name='Coördineren'),
    'Uitvoeren': dest.Phase.objects.get(name='Uitvoeren'),
    'Afhandelen': dest.Phase.objects.get(name='Afhandelen'),
}

ARRAY_FIELDS = [
    'organisatorische_aspecten',
    'uitvoeringsscenario',
    'soort_afwijking',
    'aanwezigen',
    'bezoekerslijst',
    'vochtigheid_1',
    'windrichting_1',
    'materieel'
]

class Command(BaseCommand):
    help = 'Import data from zs'

    def add_arguments(self, parser):
        parser.add_argument('--database-url', type=str,
                            help='The URL of the database to import from')
        parser.add_argument('--storage-path', type=str,
                            help='The path where the storage resides',
                            default='/var/tmp/zs/storage')

    def handle(self, database_url, storage_path, *args, **kwargs):
        self.storage_path = storage_path
        self.engine = create_engine(database_url, pool_recycle=3600)
        self.session = sessionmaker(bind=self.engine)()

        self.import_users()
        self.import_cases()

    def import_users(self):
        for user in self.session.query(src.UserEntity).join(src.Subject).all():
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

    def import_cases(self):
        for zaak in self.session.query(src.Zaak).filter(src.Zaak.zaaktype_id.in_([7,8])):
            print('Importing {}'.format(zaak.id))

            src_data = self.session.query(src.ObjectData).filter_by(object_class='case', object_id=zaak.id).first()
            if not src_data or not src_data.properties.get('values'):
                continue

            processed_data = self.process_case_data(src_data.properties['values'])

            processed_data['data']['dagwerkzaamheden'] = []
            for subzaak in self.session.query(src.Zaak).filter_by(zaaktype_id=9, pid=zaak.id):
                subzaak_data = self.session.query(src.ObjectData).filter_by(object_class='case', object_id=subzaak.id).first()
                if not subzaak_data:
                    continue

                processed_subzaak_data = self.process_case_data(subzaak_data.properties['values'])
                processed_subzaak_data['data']['datum'] = subzaak.registratiedatum.isoformat()[:10]
                processed_data['data']['dagwerkzaamheden'].append(processed_subzaak_data['data'])

            case, _ = dest.Case.objects.update_or_create(
                pk=zaak.id,
                defaults={
                    'case_type': DEST_CASE_TYPE,
                    'current_phase': processed_data['current_phase'],
                    'assignee': processed_data['assignee'],
                    'data': processed_data['data'],
                    'created_at': zaak.created,
                }
            )

            for log_record in self.session.query(src.Logging).filter_by(zaak_id=zaak.id).all():
                self.import_log_record(case, log_record)

            for file in self.session.query(src.File).filter_by(case_id=zaak.id).join(src.Filestore).all():
                self.import_file(case, file)

    def process_case_data(self, values):
        data = {}

        for key, content in values.items():
            if key.startswith('attribute.'):
                if type(content['value']) == dict:
                    if content['value'].get('__DateTime__'):
                        value = content['value']['__DateTime__'][:10] if len(content['value']) > 0 else ''
                    else:
                        value = content['value']
                elif type(content['value']) == list:
                    if key[10:] in ARRAY_FIELDS:
                        value = content['value']
                    else:
                        value = content['value'][0] if len(content['value']) > 0 else None
                else:
                    value = content['value']

                data[key[10:]] = value
            if key == 'case.phase':
                current_phase = CASE_PHASE_MAPPING.get(content['value'], None)
            if key == 'case.assignee.id':
                try:
                    assignee = dest.User.objects.get(id=content['value'])
                except dest.User.DoesNotExist:
                    assignee = None

        return {
            'data': data,
            'current_phase': current_phase,
            'assignee': assignee
        }

    def import_log_record(self, case, log_record):
        regex_result = re.findall(r'betrokkene-medewerker-(\d+)', log_record.created_by or '')
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
                    'performer': performer.to_dict()
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
                    'performer': performer.to_dict()
                }
            )
        elif log_record.event_type == 'case/accept':
            case.logs.update_or_create(
                pk=log_record.id,
                defaults={
                    'event': 'claim_case',
                    'created_at': log_record.created,
                    'performer': performer.to_dict()
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
                    'performer': performer.to_dict()
                }
            )

    def import_file(self, case, file):
        file_path = os.path.join(
            self.storage_path,
            file.filestore.uuid[0],
            file.filestore.uuid[1],
            file.filestore.uuid[2],
            file.filestore.uuid[3],
            file.filestore.uuid[4],
            'zs_{}'.format(file.filestore.uuid)
        )

        try:
            with open(file_path, 'rb') as local_file:
                case.attachments.get_or_create(
                    pk=file.id,
                    defaults={
                        'name': file.filestore.original_name,
                        'file': File(local_file, name=file.filestore.original_name),
                        'created_at': file.date_created
                    }
                )
        except FileNotFoundError:
            self.stdout.write('Could not find file {}'.format(file_path))

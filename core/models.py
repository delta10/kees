import os
import html
from importlib import import_module
from django.contrib.postgres.fields import JSONField
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.core.mail import send_mail
from django.template import Template, Context
from .lib import get_actions_from_apps


class Manager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, external_id=None, is_active=True):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        if is_active:
            user.is_active = True

        if password:
            user.set_password(password)

        if external_id:
            user.external_id = external_id

        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = Manager()

    username = models.CharField(_('gebruikersnaam'), max_length=255, unique=True)
    email = models.EmailField(max_length=255)

    initials = models.CharField(_('initials'), max_length=10, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    company = models.CharField(_('bedrijf'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('telefoonnummer'), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(_('is actief'), default=True)
    last_visit = models.DateTimeField(_('laatste bezoek'), null=True)

    external_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company
        }

    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email or settings.FROM_EMAIL, [
            self.email
        ], **kwargs)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.username)

    class Meta:
        verbose_name = _('Gebruiker')
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Case(models.Model):
    name = models.CharField(_('naam'), max_length=255)
    case_type = models.ForeignKey('CaseType', on_delete=models.PROTECT, verbose_name=_('zaaktype'))
    created_at = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=_('aangemaakt op'))
    current_phase = models.ForeignKey('Phase', on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('Huidige fase'))
    assignee = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('Behandelaar'))
    data = JSONField(default=dict, blank=True)

    def save(self, *args, **kwargs):
        self.name = html.unescape(Template(self.case_type.display_name).render(Context(self.data)))

        if not self.id:
            self.current_phase = self.case_type.phases.all()[1]

        super(Case, self).save(*args, **kwargs)

    def close(self):
        self.current_phase = None
        self.assignee = None

        return self.save()

    def next_phase(self, request):
        phases = list(self.case_type.phases.all())

        if self.current_phase:
            old_index = phases.index(self.current_phase)
            new_phase = phases[old_index + 1]
            self.execute_actions(request)
        else:
            new_phase = phases[1]

        self.current_phase = new_phase

        return self.save()

    @property
    def first_phase(self):
        return self.case_type.phases.first()

    @property
    def last_phase(self):
        return self.case_type.phases.last()

    @property
    def is_open(self):
        return self.current_phase is not None

    @property
    def is_closed(self):
        return self.current_phase is None

    def execute_actions(self, request):
        result = True

        for action in self.current_phase.actions.all():
            if not action.meets_conditions(self):
                continue

            mod = import_module(action.key)
            cls = getattr(mod, 'Action')
            instance = cls()

            if not instance.execute(self, {**action.args, 'user': request.user}):
                result = False

        return result

    class Meta:
        verbose_name = _('Zaak')
        verbose_name_plural = _('Zaken')
        ordering = ['-created_at']

        permissions = (
            ('can_manage_cases', 'Can manage cases'),
        )

    def __str__(self):
        return '#{}: {}'.format(self.id, self.name)


class CaseType(models.Model):
    name = models.CharField(_('naam'), max_length=255)
    display_name = models.CharField(_('weergavenaam van zaak'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Zaaktype')


class CaseLog(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='logs', verbose_name=_('zaak'))
    event = models.CharField(_('gebeurtenis'), max_length=255)
    performer = JSONField(_('uitgevoerd door'), default=dict, blank=True)
    created_at = models.DateTimeField(_('datum/tijd'), default=timezone.now, db_index=True)
    metadata = JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def display_performer(self):
        return '{} {} ({})'.format(
            self.performer.get('first_name'),
            self.performer.get('last_name'),
            self.performer.get('username')
        )

    @property
    def display_event(self):
        events = {
            'change_phase': _('Fase aangepast naar %s' % self.metadata.get('new_phase')),
            'next_phase': _('Fase doorgezet naar %s' % self.metadata.get('new_phase')),
            'create_attachment': _('Bijlage %s toegevoegd' % self.metadata.get('attachment_name')),
            'delete_attachment': _('Bijlage %s verwijderd' % self.metadata.get('attachment_name')),
            'change_assignee': _('Behandelaar gewijzigd naar %s' % self.metadata.get('assignee_name', '-')),
            'claim_case': _('Zaak in behandeling genomen'),
            'create_case': _('Zaak aangemaakt'),
            'closed_case': _('Zaak gesloten'),
            'mozard_request': _('Externe koppeling: Zaak aangemaakt op %s onder nummer %s' % (self.metadata.get('host'), self.metadata.get('mozard_case_id'))),
            'http_request': _('Externe koppeling: %s' % self.metadata.get('message', '-')),
            'send_email': _('E-mail koppeling: Verstuurd naar %s met onderwerp %s' % (self.metadata.get('email_to'), self.metadata.get('subject')))
        }

        return events.get(self.event, self.event)


class Phase(models.Model):
    case_type = models.ForeignKey('CaseType', on_delete=models.PROTECT, related_name='phases', verbose_name=_('zaaktype'))
    order = models.IntegerField(_('volgorde'))
    name = models.CharField(_('naam'), max_length=255)
    fields = JSONField(_('velden'), default=list, blank=True)
    assign_to = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('wijs toe aan groep'))

    class Meta:
        verbose_name = 'Fase'
        ordering = ['case_type', 'order']

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_TYPES = (
        ('ArrayField', 'ArrayField'),
        ('ArrayTextField', 'ArrayTextField'),
        ('CheckboxField', 'CheckboxField'),
        ('DateField', 'DateField'),
        ('Heading', 'Heading'),
        ('NumberField', 'NumberField'),
        ('RadioField', 'RadioField'),
        ('SelectField', 'SelectField'),
        ('Template', 'Template'),
        ('TextareaField', 'TextareaField'),
        ('TextField', 'TextField'),
    )

    case_type = models.ForeignKey('CaseType', on_delete=models.PROTECT, verbose_name=_('zaaktype'))
    key = models.SlugField(max_length=50, verbose_name=_('sleutel'))

    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=FIELD_TYPES)
    initial = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('beginwaarde'))
    args = JSONField(default=dict, blank=True, verbose_name=_('instellingen'))

    class Meta:
        verbose_name = _('Veld')
        verbose_name_plural = _('Velden')
        unique_together = ['case_type', 'key']
        ordering = ['case_type', 'key']

    def __str__(self):
        return self.label

    def toDict(self):
        return {
            'key': self.key,
            'label': self.label,
            'type': self.type,
            'initial': self.initial,
            'args': self.args
        }


class Action(models.Model):
    phase = models.ForeignKey('Phase', on_delete=models.PROTECT, related_name='actions', verbose_name=_('fase'))
    key = models.CharField(max_length=255, choices=lazy(get_actions_from_apps, tuple)(), verbose_name=_('type'))
    conditions = JSONField(default=dict, blank=True, verbose_name=('voorwaarden'))
    args = JSONField(default=dict, blank=True, verbose_name=_('instellingen'))

    class Meta:
        verbose_name = _('Actie')

    def __str__(self):
        return self.key

    def meets_conditions(self, case):
        for key, condition in self.conditions.items():
            if condition.get("is"):
                if case.data.get(key) != condition.get("is"):
                    return False
            if condition.get("isNot"):
                if case.data.get(key) == condition.get("is"):
                    return False

        return True


def upload_to(instance, filename):
    dirname = instance.created_at.strftime('attachments/%Y/%m/%d/')
    return os.path.join(dirname, get_random_string(length=24), filename)

class Attachment(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='attachments')
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=upload_to)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.file.name)

        super(Attachment, self).save(*args, **kwargs)

    @property
    def display_name(self):
        if self.name:
            return self.name

        return os.path.basename(self.file.name)

    @property
    def extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension.replace('.', '')

    class Meta:
        ordering = ['-id']
        verbose_name = _('Bijlage')


class PredefinedFilter(models.Model):
    name = models.CharField(_('naam'), max_length=255)
    args = JSONField(_('instellingen'), default=dict, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Voorgedefinieerde filter')

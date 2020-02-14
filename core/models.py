import os
import html
from importlib import import_module
from django.contrib.postgres.fields import JSONField
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)

    initials = models.CharField(_('initials'), max_length=10, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    last_visit = models.DateTimeField(null=True)

    external_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.name

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
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Case(models.Model):
    name = models.CharField(max_length=255)
    case_type = models.ForeignKey('CaseType', on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    current_phase = models.ForeignKey('Phase', on_delete=models.PROTECT, null=True, blank=True)
    assignee = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True)
    data = JSONField(default=dict, blank=True)

    def save(self, *args, **kwargs):
        self.name = html.unescape(Template(self.case_type.display_name).render(Context(self.data)))

        if not self.id:
            self.current_phase = self.case_type.phases.all()[1]

        super(Case, self).save(*args, **kwargs)

    def close(self):
        self.current_phase = None
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
            mod = import_module(action.key)
            cls = getattr(mod, 'Action')
            instance = cls()

            if not instance.execute(self, {**action.args, 'user': request.user}):
                result = False

        return result

    class Meta:
        ordering = ['-created_at']

        permissions = (
            ('can_manage_cases', 'Can manage cases'),
        )

    def __str__(self):
        return '#{}: {}'.format(self.id, self.name)


class CaseType(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CaseLog(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='logs')
    event = models.CharField(max_length=255)
    performer = models.ForeignKey('User', on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    metadata = JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']


class Phase(models.Model):
    case_type = models.ForeignKey('CaseType', on_delete=models.PROTECT, related_name='phases')
    order = models.IntegerField()
    name = models.CharField(max_length=255)
    fields = JSONField(default=list, blank=True)

    class Meta:
        ordering = ['case_type', 'order']

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_TYPES = (
        ('ArrayField', 'ArrayField'),
        ('CharField', 'CharField'),
        ('IntegerField', 'IntegerField'),
        ('DateField', 'DateField'),
        ('TimeField', 'TimeField'),
        ('DateTimeField', 'DateTimeField'),
        ('DurationField', 'DurationField'),
        ('EmailField', 'EmailField'),
        ('URLField', 'URLField'),
        ('BooleanField', 'BooleanField'),
        ('ChoiceField', 'ChoiceField'),
        ('MultipleChoiceField', 'MultipleChoiceField'),
        ('FloatField', 'FloatField'),
        ('DecimalField', 'DecimalField'),
        ('Template', 'Template'),
    )

    FIELD_WIDGETS = (
        ('TextInput', 'TextInput'),
        ('NumberInput', 'NumberInput'),
        ('EmailInput', 'EmailInput'),
        ('URLInput', 'URLInput'),
        ('Textarea', 'Textarea'),
        ('DateInput', 'DateInput'),
        ('DateTimeInput', 'DateTimeInput'),
        ('TimeInput', 'TimeInput'),
        ('CheckboxInput', 'CheckboxInput'),
        ('Select', 'Select'),
        ('SelectMultiple', 'SelectMultiple'),
        ('RadioSelect', 'RadioSelect'),
        ('CheckboxSelectMultiple', 'CheckboxSelectMultiple'),
    )

    case_type = models.ForeignKey('CaseType', on_delete=models.PROTECT)
    key = models.SlugField(max_length=50)

    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=FIELD_TYPES)
    widget = models.CharField(max_length=255, choices=FIELD_WIDGETS, blank=True, null=True)
    initial = models.CharField(max_length=255, blank=True, null=True)
    args = JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ['case_type', 'key']
        ordering = ['case_type', 'key']

    def __str__(self):
        return self.label

    def toDict(self):
        return {
            'key': self.key,
            'label': self.label,
            'type': self.type,
            'widget': self.widget,
            'initial': self.initial,
            'args': self.args
        }


class Action(models.Model):
    phase = models.ForeignKey('Phase', on_delete=models.PROTECT, related_name='actions')
    key = models.CharField(max_length=255, choices=lazy(get_actions_from_apps, tuple)())
    args = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.key


def upload_to(instance, filename):
    dirname = instance.created_at.strftime('attachments/%Y/%m/%d/')
    return os.path.join(dirname, get_random_string(length=24), filename)

class Attachment(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='attachments')
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=upload_to)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-id']

    @property
    def display_name(self):
        if self.name:
            return self.name

        return os.path.basename(self.file.name)

    @property
    def extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension.replace('.', '')

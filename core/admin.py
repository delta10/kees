from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.forms import ModelForm
from reversion.admin import VersionAdmin

from .models import User, Case, CaseType, Phase, Field, Action, PredefinedFilter
from .formfields import JSONEditor


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'company', 'email', 'groepen', 'last_visit')
    list_filter = ('is_superuser', )
    ordering = ('first_name', 'last_name', )
    filter_horizontal = ()

    readonly_fields = ('last_visit', )

    def groepen(self, user):
        groups = user.groups.all()

        if len(groups) > 0:
            return ', '.join([group.name for group in groups])

        return ''

    fieldsets = (
        (None, {'fields': ('username', 'password', 'last_visit')}),
        (_('Personal info'), {'fields': ('initials', 'first_name', 'last_name', 'email', 'company', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'groups')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password',
                'initials',
                'first_name',
                'last_name',
                'email',
                'company',
                'phone',
            ),
        }),
    )

    actions = []


class CaseAdmin(VersionAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'case_type', 'order', )
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


class FieldAdmin(admin.ModelAdmin):
    list_display = ('key', 'label', 'type', 'case_type', )
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


class ActionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


class PredefinedFilterAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


admin.site.register(User, UserAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseType)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(PredefinedFilter, PredefinedFilterAdmin)

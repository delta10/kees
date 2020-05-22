from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from django.forms import ModelForm
from reversion.admin import VersionAdmin

from .models import User, Case, CaseType, Phase, Field, Action, PredefinedFilter
from .formfields import JSONEditor


def create_add_to_group(group):
    def add_to_group(modeladmin, request, queryset):
        for user in queryset:
            user.groups.add(group)

    add_to_group.short_description = "Voeg toe aan groep {0}".format(group)
    add_to_group.__name__ = 'add_to_group_{0}'.format(group.id)

    return add_to_group

def create_delete_from_group(group):
    def delete_from_group(modeladmin, request, queryset):
        for user in queryset:
            user.groups.remove(group)

    delete_from_group.short_description = "Verwijder uit groep {0}".format(group)
    delete_from_group.__name__ = 'delete_from_group_{0}'.format(group.id)

    return delete_from_group


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
    list_filter = ('is_superuser', 'is_active', 'groups')
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

    def get_actions(self, request):
        actions = super().get_actions(request)

        for group in Group.objects.all():
            action = create_add_to_group(group)
            actions[action.__name__] = (
                action,
                action.__name__,
                action.short_description
            )

            action = create_delete_from_group(group)
            actions[action.__name__] = (
                action,
                action.__name__,
                action.short_description
            )

        return actions


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

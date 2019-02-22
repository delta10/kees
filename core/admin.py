from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.forms import ModelForm

from .models import User, Case, CaseType, Phase, PhaseField, Action, CaseLog, Attachment


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'name', )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('name', 'username', 'email', 'last_visit')
    list_filter = ('is_superuser', )
    ordering = ('name', )
    filter_horizontal = ()

    readonly_fields = ('last_visit', )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'last_visit')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'groups')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'email', 'name'),
        }),
    )

    actions = []


class PhaseAdmin(admin.ModelAdmin):
    list_display = ('case_type', 'name', 'order')


class PhaseFieldAdmin(admin.ModelAdmin):
    list_display = ('phase', 'label', 'order')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('case', 'file')


admin.site.register(User, UserAdmin)
admin.site.register(Case)
admin.site.register(CaseType)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(PhaseField, PhaseFieldAdmin)
admin.site.register(Action)
admin.site.register(CaseLog)
admin.site.register(Attachment, AttachmentAdmin)

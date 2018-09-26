from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.forms import ModelForm

from .models import User

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
    list_filter = ('is_admin', )
    ordering = ('name', )
    filter_horizontal = ()

    readonly_fields = ('last_visit', )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'last_visit')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'email', 'name'),
        }),
    )

    actions = []

# Register your models here.
admin.site.register(User, UserAdmin)

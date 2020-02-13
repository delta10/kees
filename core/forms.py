from django import forms
from .models import Case, Attachment


class ChangeAssigneeForm(forms.ModelForm):
    def __init__(self, case, *args, **kwargs):
        super(ChangeAssigneeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['assignee']


class ChangePhaseForm(forms.ModelForm):
    def __init__(self, case, *args, **kwargs):
        super(ChangePhaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['current_phase']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

from django import forms
from .models import Case, Attachment


class PhaseForm(forms.Form):
    def __init__(self, phase, *args, **kwargs):
        super(PhaseForm, self).__init__(*args, **kwargs)

        for field in phase.fields.all():
            field_args = field.args

            if field.widget:
                field_args['widget'] = getattr(forms, field.widget)

            self.fields[field.key] = getattr(forms, field.type)(label=field.label, initial=field.initial, **field_args)


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

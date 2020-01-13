from django import forms
from .models import Case, Field, Attachment


class PhaseForm(forms.Form):

    INPUT_TYPES = {
        'DateInput': 'date',
        'TimeInput': 'time',
        'DateTimeInput': 'datetime-local',
    }

    def __init__(self, phase, *args, **kwargs):
        super(PhaseForm, self).__init__(*args, **kwargs)

        for field in [Field.objects.get(key=key) for key in phase.fields]:
            field_args = field.args

            if field.widget:
                widget = getattr(forms, field.widget)

                if field.widget in self.INPUT_TYPES:
                    widget = widget(attrs={'type': self.INPUT_TYPES[field.widget]})

                field_args['widget'] = widget

            if isinstance(field_args.get('choices'), list) and not isinstance(field_args['choices'][0], list):
                field_args['choices'] = [
                    *[[i, i] for i in field_args['choices']]
                ]

            if field.widget in ['Select', 'SelectMultiple']:
                field_args['choices'] = [
                    [None, ''],
                    *field_args['choices']
                ]

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

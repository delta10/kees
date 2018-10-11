from django import forms

class PhaseForm(forms.Form):
    def __init__(self, phase, *args, **kwargs):
        super(PhaseForm, self).__init__(*args, **kwargs)

        for field in phase.fields.all():
            field_args = field.args

            if field.widget:
                field_args['widget'] = getattr(forms, field.widget)

            self.fields[field.key] =  getattr(forms, field.type)(label=field.label, initial=field.initial, **field_args)
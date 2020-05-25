from django import forms
from .models import Case, Attachment


class ChangeAssigneeForm(forms.ModelForm):
    def __init__(self, case, *args, **kwargs):
        super(ChangeAssigneeForm, self).__init__(*args, **kwargs)

        self.fields['assignee'].widget.attrs.update({
            'data-bootstrap-select': 'true',
            'data-live-search': 'true',
        })

    class Meta:
        model = Case
        fields = ['assignee']


class ChangeManagerForm(forms.ModelForm):
    def __init__(self, case, *args, **kwargs):
        super(ChangeManagerForm, self).__init__(*args, **kwargs)

        self.fields['manager'].widget.attrs.update({
            'data-bootstrap-select': 'true',
            'data-live-search': 'true',
        })

    class Meta:
        model = Case
        fields = ['manager']


class ChangePhaseForm(forms.ModelForm):
    def __init__(self, case, *args, **kwargs):
        super(ChangePhaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['current_phase']


class AttachmentForm(forms.ModelForm):
    def __init__(self, data=None, files=None, attachment_type='file', **kwargs):
        super().__init__(data, files, **kwargs)
        self.fields['file'].widget.attrs.update({
            'multiple': True,
        })

        if attachment_type == 'image':
            self.fields['file'].widget.attrs.update({
                'accept': 'image/*',
            })

    def save(self, case, *args, **kwargs):
        attachments = []
        for file in self.files.getlist('file'):
            attachment = case.attachments.create(
                file=file,
                name=file.name
            )
            attachments.append(attachment)

        return attachments

    class Meta:
        model = Attachment
        fields = ['file']

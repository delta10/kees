import json
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt


class JSONEditor(Textarea):
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.1/jsoneditor.js',
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
            'admin/js/jsoneditor.init.js',
        )
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.1/jsoneditor.css',
                'admin/css/jsoneditor.init.css',
            )
        }

    def render(self, name, value, attrs=None, renderer=None):
        if not isinstance(value, (str, bytes)):
            value = json.dumps(value)

        html = super(JSONEditor, self).render(name, value, {
            'hidden': True
        })

        div_attrs = {
            'class': 'jsoneditor-container',
            'data-jsoneditor': name,
        }

        html += '''
        <div %(attrs)s></div>
        ''' % {
            'attrs': flatatt(div_attrs),
        }

        return mark_safe(html)

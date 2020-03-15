from datetime import datetime
from django import template
from django.utils.formats import date_format

register = template.Library()

@register.filter(name='display_field')
def display_field(data, field):
    value = data.get(field.key, '')

    if field.type == 'DateField':
        return _date_format(value)

    return value

def _date_format(value):
    if not value:
        return ''

    date = datetime.fromisoformat(value)
    return date_format(date, 'SHORT_DATE_FORMAT')

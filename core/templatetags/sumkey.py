from django import template

register = template.Library()


@register.filter(name='sumkey')
def sumkey(values, key):
    return sum([to_float(item.get(key)) for item in values])

def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError, OverflowError):
        return 0

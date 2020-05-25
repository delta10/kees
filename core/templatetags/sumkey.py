from django import template

register = template.Library()


@register.filter(name='sumkey')
def sumkey(values, key):
    return sum([(int(item.get(key)) if item.get(key) else 0) for item in values])

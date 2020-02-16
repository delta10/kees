from django import template

register = template.Library()


@register.filter(name='sumkey')
def sumkey(values, key):
    return sum([int(item.get(key, 0)) for item in values])

from django.template.defaulttags import register

@register.filter
def get_index(input_list, key):
    try:
        return list(input_list).index(key)
    except ValueError:
        return -1

from django import template
register = template.Library()
@register.filter
def split(str, key):
    return str.split(key)[0]

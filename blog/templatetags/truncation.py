from django import template

register = template.Library()

@register.filter
def truncatedwords(value, arg):
    return " ".join(value.split()[arg:])
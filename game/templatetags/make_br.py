from django import template

register = template.Library()

@register.filter
def make_br(value):
    return value.replace("\n","<br />")
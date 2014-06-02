from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def django_settings(name):
    if name in getattr(settings, 'TEMPLATE_READABLE_VALUES', []):
        return getattr(settings, name, '')
    return ''

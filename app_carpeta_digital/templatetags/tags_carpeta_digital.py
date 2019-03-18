from django import template
from django.urls import reverse

register = template.Library()


@register.filter(name='is_url_active')
def is_url_active(url, request):
    return  request.path.startswith(reverse(url))

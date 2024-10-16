from django import template
from theme.models import Setting, SocialLink

register = template.Library()

@register.filter
def settings(request):
    info = Setting.objects.all()
    return info

@register.filter
def social_links(request):
    link = SocialLink.objects.filter(is_active=True)
    return link

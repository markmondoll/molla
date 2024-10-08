from django import template
from theme.models import Setting, SocialLink

register = template.Library()

@register.filter
def settings(request):
    setting = Setting.objects.all()

@register.filter
def social_links(request):
    setting = SocialLink.objects.all()


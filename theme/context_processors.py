from .models import Setting, SocialLink
from store.models import Category

def settings_info(request):
    categories = Category.objects.all()

    settings = Setting.objects.all()
    social_links = SocialLink.objects.all()

    context = {
        'categories': categories,
        'settings': settings,
        'social_links': social_links,
    }
    return context
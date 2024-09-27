from django.contrib import admin
from theme.models import Setting, SocialLink, EmailList

admin.site.register(Setting)
admin.site.register(SocialLink)
admin.site.register(EmailList)

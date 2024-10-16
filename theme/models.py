from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website_title = models.CharField(max_length=30, null=True, blank=True)
    slogan = models.CharField(max_length=200, null=True, blank=True)
    address_line1 = models.CharField(max_length=90, null=True, blank=True)
    address_line2 = models.CharField(max_length=90, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(upload_to="settings/", blank=True, null=True)
    favicon_ico = models.ImageField(upload_to="settings/", blank=True, null=True)
    favicon_png = models.ImageField(upload_to="settings/", blank=True, null=True)
    apple_touch_icon_png = models.ImageField(upload_to="settings/", blank=True, null=True)
    map_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.website_title
    

class SocialLink(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=True, null=True)
    logo = models.ImageField(upload_to="social_link/", blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class EmailList(models.Model):
    email_list = models.EmailField(max_length=250)
    
    def __str__(self):
        return self.email_list
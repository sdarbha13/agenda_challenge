from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save, pre_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.conf import settings
import urllib.parse
from .enums import ProfileTypes



class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=512, default="", blank=True)

    @property
    def get_html_url(self):
        url = reverse('uva_guide:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    def get_maps_url(self):
        return "https://www.google.com/maps/search/?api=1&query="+urllib.parse.quote_plus(self.location)

    def __str__(self):
        return "Event: " + self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = User.get_email_field_name()
    firstTime = models.BooleanField(default=True)
    type = models.CharField(
        max_length=255,
        choices=ProfileTypes.choices,
        default=ProfileTypes.STUDENT,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Org(models.Model):  # Shortened to "Org" to avoid confusion on spelling of Organiz(s)ation
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    adminList = []
    adminList.append(Profile.email)
   #content_type = ContentType.objects.get(app_label='auth', model='user')
    #Permission.objects.create(codename=name, name='Org_Admin', content_type=content_type)   #Come back and fix?
    #Profile.user.user_permissions.add(permission)
    def __str__(self):
        return "Org: " + self.name


class OrgType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    orgs = models.ManyToManyField(Org, related_name="type")
    class Meta:
        verbose_name_plural = "Org Types"  # name of the table in admin side
    def __str__(self):
        return "OrgType: " + self.name
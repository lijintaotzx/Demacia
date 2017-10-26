# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
# Create your models here.

def upload_to(instance, filename):
    return '/'.join([settings.MEDIA_ROOT, instance.user_name, filename])

def user_directory_path(instance, filename):
    date_path = datetime.date.today().strftime('%Y/%m/%d/')
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}/'.format(instance.user.username, date_path, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile')
    phone_num = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=8, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    descr = models.CharField(max_length=256, blank=True, null=True)
    head_photo = models.ImageField(upload_to=user_directory_path,null=True)


def userprofile_init(sender, instance, created, **kwargs):
    if created:
        print instance.id
        UserProfile.objects.create(user=instance)
        print 'userprofile create successful!'

post_save.connect(userprofile_init, sender=User)
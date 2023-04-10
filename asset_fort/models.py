import random
import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from tinymce.models import HTMLField


def asset_image_rename(instance, filename):
    upload_to = 'asset/images'
    ext = filename.split('.')[-1]
    filename = f'{instance.pk}.{ext}' if instance.pk else f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)


class CategoryModel(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    
    
class AssetModel(models.Model):
    serial_num = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='assets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_assets')
    asset_manufacturer = models.CharField(max_length=100)
    description = HTMLField()
    asset_image = models.ImageField(default="default.jpeg", upload_to = asset_image_rename)
    date_purchased = models.DateTimeField()
    asset_issued = models.IntegerField(default=0)
    asset_available = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


 # category slug generator
@receiver(pre_save, sender=CategoryModel)
def category_slug_pre_save_receiver(sender, instance, *args, **kwargs):

    name = slugify(instance.title.lower())
    if prev_slug := not CategoryModel.objects.filter(slug__exact=name).exists():
        slug_binding = name
    else:
        slug_binding = f"{name}-{random.randint(0, 1000)}"
    instance.slug = slug_binding

 # asset slug generator
@receiver(pre_save, sender=AssetModel)
def asset_slug_pre_save_receiver(sender, instance, *args, **kwargs):

    name = slugify(instance.title.lower())
    if prev_slug := not AssetModel.objects.filter(slug__exact=name).exists():
        slug_binding = name
    else:
        slug_binding = f"{name}-{random.randint(0, 1000)}"
    instance.slug = slug_binding    
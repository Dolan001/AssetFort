import random

from django.db import models
from django.dispatch import receiver

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save, pre_save


class CategoryModel(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    
    
@receiver(pre_save, sender=CategoryModel)
def category_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    # ==================================
    # blog slug generator
    # ==================================
    """

    name = slugify(instance.title.lower())
    if prev_slug := not CategoryModel.objects.filter(slug__exact=name).exists():
        slug_binding = name
    else:
        slug_binding = f"{name}-{random.randint(0, 1000)}"
    instance.slug = slug_binding
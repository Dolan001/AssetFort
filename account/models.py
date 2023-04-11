import os
import random
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from tinymce.models import HTMLField


def company_image_rename(instance, filename):
    upload_to = 'company/images'
    ext = filename.split('.')[-1]
    filename = f'{instance.pk}.{ext}' if instance.pk else f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)

def employee_image_rename(instance, filename):
    upload_to = 'employee/images'
    ext = filename.split('.')[-1]
    filename = f'{instance.pk}.{ext}' if instance.pk else f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)

# Company information fields
class CompanyModel(models.Model):
    title = models.CharField(max_length=100)
    description = HTMLField()
    slug = models.SlugField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='company_user')
    contact_no = models.CharField(max_length=50)
    location = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    image = models.ImageField(default="default.jpeg", upload_to=company_image_rename)

    def __str__(self):
        return self.title
    
# Employee information fields
class EmployeeModel(models.Model):
    employee_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.ForeignKey(CompanyModel, on_delete= models.CASCADE, related_name='company_employee')
    job_description = HTMLField()
    image = models.ImageField(default="default.jpeg", upload_to=employee_image_rename)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.employee_id

# company slug generator
@receiver(pre_save, sender=CompanyModel)
def company_slug_pre_save_receiver(sender, instance, *args, **kwargs):

    name = slugify(instance.title.lower())
    if prev_slug := not CompanyModel.objects.filter(slug__exact=name).exists():
        slug_binding = name
    else:
        slug_binding = f"{name}-{random.randint(0, 1000)}"
    instance.slug = slug_binding
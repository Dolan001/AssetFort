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

from account.models import CompanyModel, EmployeeModel


def asset_image_rename(instance, filename):
    upload_to = 'asset/images'
    ext = filename.split('.')[-1]
    filename = f'{instance.pk}.{ext}' if instance.pk else f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)


ASSET_CONDITION = [
    ('NONE', 'None'),
    ('VERY_GOOD', 'No maintenance required'),
    ('GOOD', 'Only normal maintenance required'),
    ('MINOR_DEFECT_ONLY', 'Minor maintenance required'),
    ('DEFECT', 'Minor maintenance required below(10%)'),
    ('MAINTENANCE_REQUIRED', 'Significant maintenance required (10-20%)'),
    ('REQUIRES_RENEWAL', 'Significant renewal/upgrade required (20-40%)'),
    ('ASSET_UNSERVICEABLE', 'Over(50%) of asset requires replacement')
]

# Categories for assets
class CategoryModel(models.Model):
    title = models.CharField(max_length=50)
    description =models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    

# Store assets    
class AssetModel(models.Model):
    serial_num = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='assets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_assets')
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='company_assets')
    asset_manufacturer = models.CharField(max_length=100)
    description = HTMLField()
    asset_image = models.ImageField(default="default.jpeg", upload_to = asset_image_rename)
    date_purchased = models.DateTimeField()
    asset_conditions = models.CharField(max_length=355, choices=ASSET_CONDITION, default='VERY_GOOD')
    asset_condition_description = HTMLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Asset Issued model
class AssetIssuedModel(models.Model):
    issue_no = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    asset = models.ForeignKey(AssetModel, on_delete=models.CASCADE, related_name='issued_asset')
    asset_assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_assignee')
    asset_assigned_to = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='employee_issued')
    assign_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_returned = models.BooleanField(default=False)
    return_asset_condition = models.CharField(max_length=355, choices=ASSET_CONDITION, default='NONE')
    return_asset_condition_description = HTMLField(blank=True, null=True)

    def __str__(self):
        return f'{self.issue_no} to {self.asset_assigned_to}'


# class AssetLogModel(models.Model):
#     issue_no = models.CharField(max_length=355)
#     asset = models.ForeignKey(AssetModel, on_delete=models.CASCADE, related_name='issued_asset_log')
#     asset_assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_assignee_log')
#     asset_assigned_to = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='employee_issued_log')
#     assign_date = models.DateTimeField(auto_now_add=True)
#     return_date = models.DateTimeField(null=True, blank=True)
#     note = models.TextField(null=True, blank=True)
#     return_asset_conditions = models.CharField(max_length=355, choices=ASSET_CONDITION, default='NONE')
#     return_asset_condition_description = HTMLField()

#     def __str__(self):
#         return f'{self.issue_no} to {self.asset_assigned_to}'


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
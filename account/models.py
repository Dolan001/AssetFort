import os
from uuid import uuid4
from django.db import models


def employee_image_rename(instance, filename):
    upload_to = 'employee/images'
    ext = filename.split('.')[-1]
    filename = f'{instance.pk}.{ext}' if instance.pk else f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)

class EmployeeModel(models.Model):
    employee_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to=employee_image_rename)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.employee_id


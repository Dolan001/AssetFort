# Generated by Django 4.2 on 2023-04-12 04:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_companymodel_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_fort', '0004_assetissued'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AssetIssued',
            new_name='AssetIssuedModel',
        ),
    ]

# Generated by Django 4.2 on 2023-04-12 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_fort', '0009_assetissuedmodel_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetissuedmodel',
            old_name='return_asset_conditions',
            new_name='return_asset_condition',
        ),
        migrations.RemoveField(
            model_name='assetissuedmodel',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='assetissuedmodel',
            name='is_returned',
        ),
        migrations.AddField(
            model_name='assetissuedmodel',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('RETURNED', 'Returned')], default='ACTIVE', max_length=100),
        ),
    ]
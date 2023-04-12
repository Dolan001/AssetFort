# Generated by Django 4.2 on 2023-04-12 13:39

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_fort', '0011_remove_assetissuedmodel_return_asset_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetissuedmodel',
            name='return_asset_condition',
            field=models.CharField(choices=[('NONE', 'None'), ('VERY_GOOD', 'No maintenance required'), ('GOOD', 'Only normal maintenance required'), ('MINOR_DEFECT_ONLY', 'Minor maintenance required'), ('DEFECT', 'Minor maintenance required below(10%)'), ('MAINTENANCE_REQUIRED', 'Significant maintenance required (10-20%)'), ('REQUIRES_RENEWAL', 'Significant renewal/upgrade required (20-40%)'), ('ASSET_UNSERVICEABLE', 'Over(50%) of asset requires replacement')], default='NONE', max_length=355),
        ),
        migrations.AddField(
            model_name='assetissuedmodel',
            name='return_asset_condition_description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]

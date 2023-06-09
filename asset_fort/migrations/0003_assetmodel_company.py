# Generated by Django 4.2 on 2023-04-11 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_rename_first_name_employeemodel_full_name_and_more'),
        ('asset_fort', '0002_assetmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetmodel',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_assets', to='account.companymodel'),
            preserve_default=False,
        ),
    ]

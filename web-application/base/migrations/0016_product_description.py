# Generated by Django 4.2.11 on 2025-03-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_remove_product_characteristics'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]

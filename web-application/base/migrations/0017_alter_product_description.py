# Generated by Django 4.2.11 on 2025-03-13 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

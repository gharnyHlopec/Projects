# Generated by Django 4.2.11 on 2025-03-17 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_remove_productimage_shared_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='base.product'),
        ),
    ]

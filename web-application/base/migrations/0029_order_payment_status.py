# Generated by Django 4.2.11 on 2025-05-20 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Оплата картой курьеру', 'Оплата картой курьеру'), ('Оплата наличными курьеру', 'Оплата наличными курьеру'), ('Оплата картой на сайте', 'Оплата картой на сайте'), ('Оплачен', 'Оплачен')], default='-', max_length=50),
        ),
    ]

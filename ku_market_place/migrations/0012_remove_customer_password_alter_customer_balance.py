# Generated by Django 4.2.7 on 2023-11-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ku_market_place', '0011_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.IntegerField(default=10000),
        ),
    ]

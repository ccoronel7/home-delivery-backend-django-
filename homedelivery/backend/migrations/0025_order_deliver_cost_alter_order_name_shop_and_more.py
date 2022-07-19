# Generated by Django 4.0.4 on 2022-07-19 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_order_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deliver_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='name_shop',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='seller_data',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='seller_location',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='wallet_shop',
            field=models.TextField(blank=True),
        ),
    ]

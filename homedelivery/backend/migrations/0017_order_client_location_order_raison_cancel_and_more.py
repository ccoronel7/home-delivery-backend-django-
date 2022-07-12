# Generated by Django 4.0.4 on 2022-07-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_order_statu'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client_location',
            field=models.TextField(default='ubicacion_generica.txt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='raison_cancel',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='seller_location',
            field=models.TextField(default='ubicacion_generica.txt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='perfil',
            name='locate_a',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='perfil',
            name='locate_l',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='statu',
            field=models.CharField(choices=[('R', 'En revision'), ('P', 'Preparando'), ('C', 'En camino'), ('E', 'Entregado'), ('X', 'Cancelado')], default='R', max_length=1),
        ),
    ]

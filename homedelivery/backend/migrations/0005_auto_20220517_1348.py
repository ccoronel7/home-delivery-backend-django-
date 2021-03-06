# Generated by Django 3.1.7 on 2022-05-17 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20220426_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoMensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('size', models.IntegerField(default=19600)),
                ('tipo', models.CharField(default='png', max_length=5)),
                ('url', models.ImageField(upload_to='mensajes')),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.TextField()),
                ('timestamp', models.CharField(max_length=5)),
                ('system', models.BooleanField(default=False)),
                ('saved', models.BooleanField(default=False)),
                ('distributed', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('disableActions', models.BooleanField(default=False)),
                ('disableReactions', models.BooleanField(default=False)),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.mensaje')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.perfil')),
            ],
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='tienda',
        ),
        migrations.RemoveField(
            model_name='tienda',
            name='perfil',
        ),
        migrations.DeleteModel(
            name='DetalleProducto',
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
        migrations.DeleteModel(
            name='Tienda',
        ),
    ]

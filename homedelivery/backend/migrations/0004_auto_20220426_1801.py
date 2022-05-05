# Generated by Django 3.1.7 on 2022-04-26 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_rename_usuario_deliver_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='perfil',
            name='wallet',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deliver',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('wallet', models.TextField()),
                ('telefono', models.CharField(max_length=32)),
                ('direcion', models.TextField()),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.tienda')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='productos')),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField(null=True)),
                ('precio', models.FloatField(default=0.0)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.producto')),
            ],
        ),
    ]

# Generated by Django 4.1.1 on 2022-09-09 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_productos', models.IntegerField()),
                ('peso_prodcutos', models.IntegerField()),
                ('estatus', models.IntegerField(choices=[(0, 'CREADO'), (1, 'RECOLECTADO'), (2, 'EN_ESTACION'), (3, 'EN_RUTA'), (4, 'ENTREGADO'), (5, 'CANCELADO')])),
            ],
        ),
    ]
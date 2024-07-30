# Generated by Django 5.0.7 on 2024-07-30 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('cedula', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('edad', models.IntegerField()),
                ('genero', models.CharField(max_length=10)),
                ('direccion', models.CharField(max_length=200)),
                ('celular', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
                ('diagnostico', models.TextField()),
                ('alergias', models.TextField()),
                ('sintomas', models.TextField()),
                ('medicacion', models.TextField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

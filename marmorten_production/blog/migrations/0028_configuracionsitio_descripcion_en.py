# Generated by Django 5.2 on 2025-05-17 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_configuracionsitio_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracionsitio',
            name='descripcion_en',
            field=models.TextField(blank=True, verbose_name='Descripción (Inglés)'),
        ),
    ]

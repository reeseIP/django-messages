# Generated by Django 4.2.7 on 2024-03-24 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0069_externalsystems_id_externalusers_system_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalusers',
            name='system',
        ),
    ]
# Generated by Django 4.2.7 on 2024-03-22 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0048_remove_externalsystems_service_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderjobs',
            name='system',
        ),
        migrations.RemoveField(
            model_name='putawayjobs',
            name='system',
        ),
    ]

# Generated by Django 4.2.7 on 2024-03-22 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0054_orderjobs_system_putawayjobs_system'),
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

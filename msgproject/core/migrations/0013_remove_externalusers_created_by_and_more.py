# Generated by Django 4.2.7 on 2024-03-24 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_externalusers_externalsystems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalusers',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='ExternalSystems',
        ),
        migrations.DeleteModel(
            name='ExternalUsers',
        ),
    ]
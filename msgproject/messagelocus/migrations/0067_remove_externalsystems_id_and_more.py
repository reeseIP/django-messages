# Generated by Django 4.2.7 on 2024-03-24 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0066_externalsystems_externalusers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalsystems',
            name='id',
        ),
        migrations.AlterField(
            model_name='externalsystems',
            name='system',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
    ]
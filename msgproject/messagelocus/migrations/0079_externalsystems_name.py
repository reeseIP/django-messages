# Generated by Django 4.2.7 on 2024-03-26 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0078_remove_externalsystems_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalsystems',
            name='name',
            field=models.CharField(default='fill', max_length=100),
            preserve_default=False,
        ),
    ]
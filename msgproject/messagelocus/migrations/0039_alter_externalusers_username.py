# Generated by Django 4.2.7 on 2024-02-12 22:15

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0038_alter_orderserialnumbers_serialno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalusers',
            name='username',
            field=models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]

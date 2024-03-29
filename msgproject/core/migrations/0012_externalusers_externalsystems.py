# Generated by Django 4.2.7 on 2024-03-23 03:01

import core.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_remove_externalusers_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('csrf_token', models.CharField(max_length=32)),
                ('sessionid', models.CharField(max_length=32)),
                ('system', models.CharField(max_length=3)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, core.models.ModelHelp),
        ),
        migrations.CreateModel(
            name='ExternalSystems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(max_length=3)),
                ('url', models.CharField(max_length=250)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.externalservices')),
            ],
            bases=(models.Model, core.models.ModelHelp),
        ),
    ]

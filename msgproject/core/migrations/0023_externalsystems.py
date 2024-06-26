# Generated by Django 4.2.7 on 2024-04-28 19:20

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_externalservices'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalSystems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=250)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='systems', to='core.externalservices')),
            ],
            bases=(models.Model, core.models.ModelHelp),
        ),
    ]

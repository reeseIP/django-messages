# Generated by Django 4.2.7 on 2024-03-22 20:13

from django.db import migrations, models
import django.db.models.deletion
import messagelocus.models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0042_orderjobs_system_putawayjobs_system'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=250)),
            ],
            bases=(models.Model, messagelocus.models.ModelHelp),
        ),
        migrations.AlterField(
            model_name='externalsystems',
            name='url',
            field=models.CharField(max_length=250),
        ),
        migrations.AddField(
            model_name='externalsystems',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='messagelocus.externalservices'),
            preserve_default=False,
        ),
    ]

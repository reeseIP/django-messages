# Generated by Django 4.2.7 on 2024-03-24 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0071_remove_externalsystems_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalusers',
            name='system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='messagelocus.externalsystems'),
            preserve_default=False,
        ),
    ]
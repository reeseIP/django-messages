# Generated by Django 4.2.7 on 2024-04-28 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_externalusers_system'),
        ('messagelocus', '0109_remove_externalusers_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderjobs',
            name='system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orderjobs', to='core.externalsystems'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='putawayjobs',
            name='system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='putawayjobs', to='core.externalsystems'),
            preserve_default=False,
        ),
    ]

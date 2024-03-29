# Generated by Django 4.2.7 on 2024-03-22 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_externalsystems_id_alter_externalsystems_system'),
        ('messagelocus', '0053_remove_orderjobs_system_remove_putawayjobs_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderjobs',
            name='system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.externalsystems'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='putawayjobs',
            name='system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.externalsystems'),
            preserve_default=False,
        ),
    ]

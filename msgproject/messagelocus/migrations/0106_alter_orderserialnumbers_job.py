# Generated by Django 4.2.7 on 2024-04-01 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0105_alter_ordertaskresults_job_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderserialnumbers',
            name='Job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messagelocus.orderjobs'),
        ),
    ]
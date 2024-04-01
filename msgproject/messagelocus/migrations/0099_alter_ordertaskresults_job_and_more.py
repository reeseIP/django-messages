# Generated by Django 4.2.7 on 2024-03-28 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0098_alter_ordertaskresults_job_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertaskresults',
            name='Job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='messagelocus.orderjobs'),
        ),
        migrations.AlterField(
            model_name='putawaytaskresults',
            name='Job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='messagelocus.putawayjobs'),
        ),
    ]

# Generated by Django 4.2.7 on 2024-03-28 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0095_rename_jobdate_putawayjobrequests_requestdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertaskresults',
            name='Job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='messagelocus.orderjobresults'),
        ),
        migrations.AlterField(
            model_name='putawaytaskresults',
            name='Job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='messagelocus.putawayjobresults'),
        ),
    ]

# Generated by Django 4.2.7 on 2024-04-01 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0102_remove_orderjobs_eventinfo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderjobresults',
            name='JobRobot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawayjobresults',
            name='JobRobot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

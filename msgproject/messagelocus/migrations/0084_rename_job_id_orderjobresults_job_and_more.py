# Generated by Django 4.2.7 on 2024-03-28 02:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0083_orderjobresults_job_id_putawayjobresults_job_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderjobresults',
            old_name='job_id',
            new_name='Job',
        ),
        migrations.RenameField(
            model_name='putawayjobresults',
            old_name='job_id',
            new_name='Job',
        ),
    ]
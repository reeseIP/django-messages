# Generated by Django 4.2.7 on 2024-03-28 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0084_rename_job_id_orderjobresults_job_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderjobresults',
            name='message',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='putawayjobresults',
            name='message',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordertaskresults',
            name='JobId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='messagelocus.orderjobresults'),
        ),
        migrations.AlterField(
            model_name='putawaytaskresults',
            name='JobId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskresults', to='messagelocus.putawayjobresults'),
        ),
    ]

# Generated by Django 4.2.7 on 2024-03-28 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0085_orderjobresults_message_putawayjobresults_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderjobresults',
            name='EventInfo',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='orderjobresults',
            name='EventType',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orderjobresults',
            name='JobMethod',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orderjobresults',
            name='JobRobot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orderjobresults',
            name='JobStation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orderjobresults',
            name='message',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawayjobresults',
            name='EventInfo',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawayjobresults',
            name='EventType',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawayjobresults',
            name='JobRobot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawayjobresults',
            name='JobStation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawayjobresults',
            name='message',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
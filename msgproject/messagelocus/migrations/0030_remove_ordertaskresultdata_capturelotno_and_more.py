# Generated by Django 4.2.7 on 2023-11-27 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0029_orderjobdata_active_putawayjobdata_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordertaskresultdata',
            name='CaptureLotNo',
        ),
        migrations.RemoveField(
            model_name='ordertaskresultdata',
            name='CaptureSerialNo',
        ),
        migrations.RemoveField(
            model_name='ordertaskresultdata',
            name='CaptureSerialNoQty',
        ),
        migrations.AddField(
            model_name='ordertaskresultdata',
            name='ItemUPC',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

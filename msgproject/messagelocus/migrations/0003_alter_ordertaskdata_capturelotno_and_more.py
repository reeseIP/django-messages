# Generated by Django 4.2.7 on 2023-11-03 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0002_alter_orderjobdata_jobpriority_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertaskdata',
            name='CaptureLotNo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='CaptureSerialNo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='CaptureSerialNoQty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom1',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom10',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom2',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom3',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom4',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom5',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom6',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom7',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom8',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='Custom9',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemColor',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemHeight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemImageUrl',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemLength',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemSize',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemStyle',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemUPC',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemWeight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemWidth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='LotNo',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='OrderId',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='OrderLineId',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='OrderTaskId',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='OrderType',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='SerialNo',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskSequence',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskSubSequence',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskTravelPriority',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskWorkArea',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskZone',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-08 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0014_alter_orderjobdata_singleunit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='putawayjobdata',
            name='JobPriority',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='CustOwner',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom1',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom10',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom2',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom3',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom4',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom5',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom6',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom7',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom8',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='Custom9',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='EventAction',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemColor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemHeight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemImageUrl',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemLength',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemSize',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemStyle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemUPC',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemWeight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='ItemWidth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='LotNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='OrderId',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='OrderLineId',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='OrderTaskId',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='OrderType',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='SerialNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='SiteId',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='TaskTravelPriority',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='TaskWorkArea',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='putawaytaskdata',
            name='TaskZone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

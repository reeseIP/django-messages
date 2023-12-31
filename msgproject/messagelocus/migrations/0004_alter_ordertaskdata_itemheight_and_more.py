# Generated by Django 4.2.7 on 2023-11-03 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0003_alter_ordertaskdata_capturelotno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemHeight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemLength',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemWeight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='ItemWidth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskSequence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskSubSequence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordertaskdata',
            name='TaskTravelPriority',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

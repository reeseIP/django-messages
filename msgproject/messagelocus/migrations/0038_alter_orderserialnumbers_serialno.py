# Generated by Django 4.2.7 on 2024-02-01 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagelocus', '0037_orderserialnumbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderserialnumbers',
            name='SerialNo',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 2.2 on 2019-08-01 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0003_auto_20190801_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dcdetailsupplier',
            name='unit_price',
        ),
    ]

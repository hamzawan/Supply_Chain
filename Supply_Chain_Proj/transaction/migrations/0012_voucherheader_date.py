# Generated by Django 2.2 on 2019-07-10 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_auto_20190710_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucherheader',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

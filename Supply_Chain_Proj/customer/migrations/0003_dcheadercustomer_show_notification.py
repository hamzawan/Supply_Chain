# Generated by Django 2.2 on 2019-06-13 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20190612_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='dcheadercustomer',
            name='show_notification',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 2.2 on 2019-05-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_auto_20190523_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartofaccount',
            name='parent_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
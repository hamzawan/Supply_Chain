# Generated by Django 2.2 on 2019-08-08 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20190803_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dcheadercustomer',
            old_name='comments',
            new_name='po_no',
        ),
    ]

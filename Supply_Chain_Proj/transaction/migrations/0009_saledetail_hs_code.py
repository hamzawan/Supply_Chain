# Generated by Django 2.2 on 2019-07-01 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0008_auto_20190630_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='saledetail',
            name='hs_code',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
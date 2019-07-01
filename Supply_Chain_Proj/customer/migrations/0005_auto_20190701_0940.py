# Generated by Django 2.2 on 2019-07-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20190630_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='dcheadercustomer',
            name='cartage_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dcheadercustomer',
            name='comments',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
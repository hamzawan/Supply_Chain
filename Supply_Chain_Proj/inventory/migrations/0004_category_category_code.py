# Generated by Django 2.2 on 2019-08-09 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20190809_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
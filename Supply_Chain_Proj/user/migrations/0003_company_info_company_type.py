# Generated by Django 2.2 on 2019-08-06 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userroles_form_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_info',
            name='company_type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

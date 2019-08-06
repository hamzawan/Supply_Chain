# Generated by Django 2.2 on 2019-08-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartage_and_Po',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartage', models.DecimalField(decimal_places=2, max_digits=8)),
                ('po_no', models.CharField(max_length=100)),
                ('invoice_id', models.IntegerField()),
            ],
        ),
    ]

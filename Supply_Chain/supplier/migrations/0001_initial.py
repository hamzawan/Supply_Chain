# Generated by Django 2.2 on 2019-05-11 07:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DcHeaderSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dc_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('mrn_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PoHeaderSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('attn', models.CharField(max_length=100)),
                ('prc_basis', models.CharField(max_length=100)),
                ('yrref', models.CharField(max_length=100)),
                ('leadtime', models.CharField(max_length=100)),
                ('validity', models.CharField(max_length=100)),
                ('payment', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=100)),
                ('exchange_rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('follow_up', models.DateField(blank=True)),
                ('show_notification', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuotationHeaderSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('attn', models.CharField(max_length=100)),
                ('prc_basis', models.CharField(max_length=100)),
                ('leadtime', models.CharField(max_length=100)),
                ('validity', models.CharField(max_length=100)),
                ('payment', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=100)),
                ('exchange_rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('follow_up', models.DateField(blank=True)),
                ('show_notification', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RfqSupplierHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfq_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('attn', models.CharField(max_length=100)),
                ('follow_up', models.DateField(blank=True)),
                ('show_notification', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RfqSupplierDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=100, unique=True)),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=100)),
                ('rfq_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.RfqSupplierHeader')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationDetailSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=100, unique=True)),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('remarks', models.CharField(max_length=100)),
                ('quotation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.QuotationHeaderSupplier')),
            ],
        ),
        migrations.CreateModel(
            name='PoDetailSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=100, unique=True)),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('remarks', models.CharField(max_length=100)),
                ('quotation_no', models.CharField(max_length=100)),
                ('po_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.PoHeaderSupplier')),
            ],
        ),
        migrations.CreateModel(
            name='DcDetailSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=100, unique=True)),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('remarks', models.CharField(max_length=100)),
                ('po_no', models.CharField(max_length=100)),
                ('dc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.DcHeaderSupplier')),
            ],
        ),
    ]

# Generated by Django 2.2 on 2019-07-16 07:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartOfAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_title', models.CharField(max_length=100, unique=True)),
                ('parent_id', models.IntegerField()),
                ('opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('phone_no', models.CharField(max_length=100)),
                ('email_address', models.CharField(max_length=100)),
                ('ntn', models.CharField(max_length=100)),
                ('stn', models.CharField(max_length=100)),
                ('cnic', models.CharField(max_length=100)),
                ('Address', models.CharField(max_length=200)),
                ('remarks', models.CharField(max_length=100)),
                ('credit_limit', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('doc_no', models.CharField(max_length=100)),
                ('doc_date', models.DateField(default=datetime.date.today)),
                ('cheque_no', models.CharField(max_length=100)),
                ('cheque_date', models.DateField(max_length=datetime.date.today)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VoucherDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount')),
                ('header_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.VoucherHeader')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refrence_id', models.CharField(max_length=100)),
                ('refrence_date', models.DateField(blank=True)),
                ('tran_type', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(default=datetime.date.today)),
                ('remarks', models.CharField(max_length=100)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount')),
            ],
        ),
        migrations.CreateModel(
            name='SaleReturnHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('footer_description', models.TextField()),
                ('payment_method', models.CharField(max_length=100)),
                ('credit_days', models.CharField(max_length=100)),
                ('cartage_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('additional_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('withholding_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount')),
            ],
        ),
        migrations.CreateModel(
            name='SaleReturnDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sales_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('dc_ref', models.CharField(max_length=100)),
                ('hs_code', models.CharField(max_length=100)),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Add_products')),
                ('sale_return_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.SaleReturnHeader')),
            ],
        ),
        migrations.CreateModel(
            name='SaleHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('footer_description', models.TextField()),
                ('payment_method', models.CharField(max_length=100)),
                ('credit_days', models.CharField(max_length=100)),
                ('cartage_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('additional_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('withholding_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('follow_up', models.DateField(blank=True)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount')),
            ],
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sales_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('dc_ref', models.CharField(max_length=100)),
                ('hs_code', models.CharField(max_length=100)),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Add_products')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.SaleHeader')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseReturnHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('footer_description', models.TextField()),
                ('payment_method', models.CharField(max_length=100)),
                ('credit_days', models.CharField(max_length=100)),
                ('cartage_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('additional_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('withholding_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseReturnDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sales_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Add_products')),
                ('purchase_return_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.PurchaseReturnHeader')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_no', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('footer_description', models.TextField()),
                ('payment_method', models.CharField(max_length=100)),
                ('credit_days', models.CharField(max_length=100)),
                ('cartage_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('additional_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('withholding_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('follow_up', models.DateField(blank=True)),
                ('account_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sales_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Add_products')),
                ('purchase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.PurchaseHeader')),
            ],
        ),
    ]

# Generated by Django 2.2 on 2019-08-03 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('inventory', '0001_initial'),
        ('transaction', '0001_initial'),
        ('supplier', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rfqsupplierheader',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount'),
        ),
        migrations.AddField(
            model_name='rfqsupplierheader',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Company_info'),
        ),
        migrations.AddField(
            model_name='rfqsupplierheader',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rfqsupplierdetail',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Add_products'),
        ),
        migrations.AddField(
            model_name='rfqsupplierdetail',
            name='rfq_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.RfqSupplierHeader'),
        ),
        migrations.AddField(
            model_name='quotationheadersupplier',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount'),
        ),
        migrations.AddField(
            model_name='quotationheadersupplier',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Company_info'),
        ),
        migrations.AddField(
            model_name='quotationheadersupplier',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotationdetailsupplier',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Add_products'),
        ),
        migrations.AddField(
            model_name='quotationdetailsupplier',
            name='quotation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.QuotationHeaderSupplier'),
        ),
        migrations.AddField(
            model_name='poheadersupplier',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount'),
        ),
        migrations.AddField(
            model_name='poheadersupplier',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Company_info'),
        ),
        migrations.AddField(
            model_name='poheadersupplier',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='podetailsupplier',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Add_products'),
        ),
        migrations.AddField(
            model_name='podetailsupplier',
            name='po_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.PoHeaderSupplier'),
        ),
        migrations.AddField(
            model_name='dcheadersupplier',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.ChartOfAccount'),
        ),
        migrations.AddField(
            model_name='dcheadersupplier',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Company_info'),
        ),
        migrations.AddField(
            model_name='dcheadersupplier',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dcdetailsupplier',
            name='dc_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.DcHeaderSupplier'),
        ),
        migrations.AddField(
            model_name='dcdetailsupplier',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Add_products'),
        ),
    ]
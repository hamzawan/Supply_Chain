# Generated by Django 2.2 on 2019-07-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_voucherdetail_invoice_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='ref_inv_tran_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2 on 2019-05-02 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20190502_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationdetailsupplier',
            name='quotation_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='supplier.QuotationHeaderSupplier'),
            preserve_default=False,
        ),
    ]

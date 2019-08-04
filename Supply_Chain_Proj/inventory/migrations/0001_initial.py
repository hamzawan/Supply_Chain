# Generated by Django 2.2 on 2019-08-03 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=100, unique=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_desc', models.TextField()),
                ('unit', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=100)),
                ('opening_stock', models.DecimalField(decimal_places=2, max_digits=8)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

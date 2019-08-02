# Generated by Django 2.2 on 2019-08-01 04:20

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
            name='FiscalYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_year', models.CharField(max_length=100)),
                ('database_name', models.CharField(max_length=100)),
                ('is_current_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_id', models.IntegerField()),
                ('form_name', models.CharField(max_length=100)),
                ('child_form', models.IntegerField()),
                ('display', models.IntegerField()),
                ('add', models.IntegerField()),
                ('edit', models.IntegerField()),
                ('delete', models.IntegerField()),
                ('r_print', models.IntegerField()),
                ('r_return', models.IntegerField(default='0')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

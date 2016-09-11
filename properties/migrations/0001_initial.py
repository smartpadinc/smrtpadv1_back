# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-11 15:25
from __future__ import unicode_literals

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
            name='UnitProperty',
            fields=[
                ('unitproperty', models.AutoField(primary_key=True, serialize=False)),
                ('property_code', models.CharField(help_text='Unique property code', max_length=30, unique=True)),
                ('property_name', models.CharField(help_text='Property name', max_length=50)),
                ('property_type', models.CharField(choices=[('1', 'Studio'), ('2', '1-Bedroom'), ('3', '2-Bedroom'), ('4', 'Villa'), ('5', 'Townhouse')], db_index=True, default='1', max_length=3)),
                ('description', models.TextField(blank=True, help_text='organization description', null=True)),
                ('address_line_1', models.CharField(blank=True, help_text='address line 1', max_length=50, null=True)),
                ('address_line_2', models.CharField(blank=True, help_text='address line 2', max_length=50, null=True)),
                ('city', models.CharField(blank=True, help_text='City', max_length=50, null=True)),
                ('state', models.CharField(blank=True, help_text='State or Province', max_length=50, null=True)),
                ('country', models.CharField(choices=[('ph', 'Philippines'), ('sg', 'Singapore')], db_index=True, default='ph', max_length=3)),
                ('zip_code', models.CharField(blank=True, help_text='Zip Code', max_length=10, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive'), ('D', 'Deleted')], db_index=True, default='A', help_text='Active / Inactive / Deleted', max_length=1)),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='Date the record was created')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the record was last edited.', null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, help_text='User who last updated the unitproperty', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unitproperty_last_updated', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(help_text='owner of the property', on_delete=django.db.models.deletion.CASCADE, related_name='property_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

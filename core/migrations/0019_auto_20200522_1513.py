# Generated by Django 3.0.6 on 2020-05-22 13:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_action_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='conditions',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='voorwaarden'),
        ),
    ]

# Generated by Django 3.0.3 on 2020-03-31 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200315_2230'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Filter',
            new_name='PredefinedFilter',
        ),
    ]
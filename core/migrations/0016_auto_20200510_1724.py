# Generated by Django 3.0.6 on 2020-05-10 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200421_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='widget',
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.CharField(choices=[('InputField', 'InputField'), ('RadioField', 'RadioField'), ('CheckboxField', 'CheckboxField'), ('SelectField', 'SelectField'), ('TextareaField', 'TextareaField'), ('ArrayField', 'ArrayField')], max_length=255),
        ),
    ]
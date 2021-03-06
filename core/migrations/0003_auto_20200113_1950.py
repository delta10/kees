# Generated by Django 2.1.1 on 2020-01-13 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200113_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phasefield',
            options={'ordering': ['case_type', 'key']},
        ),
        migrations.AddField(
            model_name='phasefield',
            name='case_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.CaseType'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='phasefield',
            unique_together={('case_type', 'key')},
        ),
    ]

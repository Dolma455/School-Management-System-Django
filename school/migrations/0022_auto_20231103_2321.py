# Generated by Django 3.0.5 on 2023-11-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0021_auto_20231103_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherextra',
            name='assigned_class',
            field=models.CharField(blank=True, choices=[('one', 'one'), ('two', 'two'), ('three', 'three'), ('four', 'four'), ('five', 'five'), ('six', 'six'), ('seven', 'seven'), ('eight', 'eight'), ('nine', 'nine'), ('ten', 'ten')], default='desc', max_length=10),
            preserve_default=False,
        ),
    ]
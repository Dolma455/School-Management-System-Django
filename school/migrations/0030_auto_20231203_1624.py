# Generated by Django 3.0.5 on 2023-12-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0029_auto_20231104_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentextra',
            name='roll',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]

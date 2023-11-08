# Generated by Django 3.0.5 on 2023-11-03 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0024_auto_20231104_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.TeacherExtra')),
                ('assigned_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Class')),
            ],
        ),
    ]

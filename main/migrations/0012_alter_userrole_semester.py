# Generated by Django 4.2.13 on 2024-07-06 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_userrole_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.semester'),
        ),
    ]

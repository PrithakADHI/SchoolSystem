# Generated by Django 4.2.13 on 2024-07-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_userrole_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.0.5 on 2022-06-18 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clone', '0009_remove_leavesandholidays_hrm_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empself',
            name='hrm_id',
        ),
    ]

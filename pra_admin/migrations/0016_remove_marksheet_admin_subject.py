# Generated by Django 4.2.4 on 2023-12-11 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pra_admin', '0015_marksheet_admin_subject_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marksheet_admin',
            name='subject',
        ),
    ]

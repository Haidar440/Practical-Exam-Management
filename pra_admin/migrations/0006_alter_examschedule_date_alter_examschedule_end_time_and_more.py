# Generated by Django 4.2.4 on 2023-09-20 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pra_admin', '0005_lab_examschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examschedule',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]

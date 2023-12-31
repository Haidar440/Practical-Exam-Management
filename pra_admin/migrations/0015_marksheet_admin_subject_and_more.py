# Generated by Django 4.2.4 on 2023-12-11 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pra_admin', '0014_marksheet_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='marksheet_admin',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.subject'),
        ),
        migrations.AlterField(
            model_name='marksheet_admin',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pra_admin.student'),
        ),
    ]

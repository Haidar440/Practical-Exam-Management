# Generated by Django 4.2.4 on 2023-12-10 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pra_admin', '0013_alter_allocation_record_batch_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marksheet_Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pratical_marks', models.IntegerField(null=True)),
                ('viva_marks', models.IntegerField(null=True)),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.division')),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pra_admin.examschedule')),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.semester')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.student')),
            ],
            options={
                'db_table': 'Admin_Marksheet',
            },
        ),
    ]

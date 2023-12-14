# Generated by Django 4.2.4 on 2023-09-20 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pra_admin', '0004_alter_student_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExamSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.division')),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pra_admin.subject')),
            ],
        ),
    ]
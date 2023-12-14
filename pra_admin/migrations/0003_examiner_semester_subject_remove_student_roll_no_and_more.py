# Generated by Django 4.2.4 on 2023-08-23 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pra_admin', '0002_alter_student_enroll_no_alter_student_roll_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examiner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'Ad_examiner',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Ad_semester',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='roll_no',
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=5),
        ),
        migrations.AddField(
            model_name='student',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pra_admin.semester'),
        ),
    ]

# Generated by Django 4.1.4 on 2023-02-12 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0004_internship_guide'),
    ]

    operations = [
        migrations.CreateModel(
            name='schedule',
            fields=[
                ('phase_no', models.IntegerField(primary_key=True, serialize=False)),
                ('phase_desc', models.CharField(max_length=100)),
                ('due_date', models.DateField()),
            ],
            options={
                'db_table': 'SCHEDULE',
            },
        ),
        migrations.CreateModel(
            name='student_sub',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('submitted_at', models.DateField(auto_now_add=True)),
                ('submission_status', models.CharField(max_length=25)),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'db_table': 'STUDENT_SUB',
            },
        ),
        migrations.AlterField(
            model_name='phase_allot',
            name='phase_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dept_project.schedule'),
        ),
    ]

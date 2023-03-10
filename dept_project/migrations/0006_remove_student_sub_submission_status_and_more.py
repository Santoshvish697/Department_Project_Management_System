# Generated by Django 4.1.4 on 2023-02-12 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0005_schedule_student_sub_alter_phase_allot_phase_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_sub',
            name='submission_status',
        ),
        migrations.AddField(
            model_name='student_sub',
            name='phase_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_sub',
            name='project_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_sub',
            name='usn',
            field=models.CharField(default='1RV20IS000', max_length=25),
        ),
        migrations.AlterField(
            model_name='phase_allot',
            name='phase_no',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dept_project.schedule'),
        ),
    ]

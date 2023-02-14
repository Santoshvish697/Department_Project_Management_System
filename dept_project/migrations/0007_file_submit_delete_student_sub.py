# Generated by Django 4.1.4 on 2023-02-13 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0006_remove_student_sub_submission_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='file_submit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase_no', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to='dept_project/static/DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/upload/')),
            ],
        ),
        migrations.DeleteModel(
            name='student_sub',
        ),
    ]
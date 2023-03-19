# Generated by Django 4.1.4 on 2023-02-15 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0011_alter_file_submit_sub_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluateResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_id', models.IntegerField(default=0)),
                ('usn', models.CharField(default='1RV20IS000', max_length=25)),
                ('rubric_1_marks', models.IntegerField(default=0)),
                ('rubric_2_marks', models.IntegerField(default=0)),
                ('rubric_3_marks', models.IntegerField(default=0)),
            ],
        ),
    ]

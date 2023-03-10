# Generated by Django 4.1.4 on 2023-02-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0003_remove_guide_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='internship_guide',
            fields=[
                ('intern_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=25)),
                ('mname', models.CharField(max_length=25)),
                ('lname', models.CharField(max_length=25)),
                ('company', models.CharField(max_length=25)),
                ('doj', models.DateField()),
            ],
            options={
                'db_table': 'INTERNSHIP_GUIDE',
            },
        ),
    ]

# Generated by Django 4.1.4 on 2023-02-13 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0008_remove_file_submit_id_file_submit_sub_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_submit',
            name='phase_no',
            field=models.IntegerField(default=1),
        ),
    ]

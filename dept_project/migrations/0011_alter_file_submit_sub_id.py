# Generated by Django 4.1.4 on 2023-02-14 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept_project', '0010_alter_file_submit_sub_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_submit',
            name='sub_id',
            field=models.IntegerField(default=100, primary_key=True, serialize=False),
        ),
    ]
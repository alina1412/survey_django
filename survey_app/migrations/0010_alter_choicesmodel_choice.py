# Generated by Django 4.0.4 on 2022-07-14 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0009_remove_choicesmodel_status_choicesmodel_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicesmodel',
            name='choice',
            field=models.CharField(choices=[('<function GetOpts.get_opts.<locals>.<lambda> at 0x00000124B6D94A60>', '<function GetOpts.get_opts.<locals>.<lambda> at 0x00000124B6D94A60>')], default='', max_length=200),
        ),
    ]

# Generated by Django 4.0.4 on 2022-07-12 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0002_rename_survey_id_question_survey'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='option',
            old_name='question_id',
            new_name='question',
        ),
    ]

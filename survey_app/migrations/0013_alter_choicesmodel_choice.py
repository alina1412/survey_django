# Generated by Django 4.0.4 on 2022-07-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0012_alter_choicesmodel_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicesmodel',
            name='choice',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

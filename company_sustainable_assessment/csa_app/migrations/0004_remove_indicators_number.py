# Generated by Django 4.0.1 on 2022-05-18 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0003_alter_indicators_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicators',
            name='number',
        ),
    ]

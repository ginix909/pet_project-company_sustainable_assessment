# Generated by Django 4.0.1 on 2022-05-18 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0002_indicators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicators',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]

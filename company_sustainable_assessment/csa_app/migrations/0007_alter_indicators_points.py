# Generated by Django 4.0.1 on 2022-06-06 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0006_alter_indicators_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicators',
            name='points',
            field=models.IntegerField(null=True),
        ),
    ]

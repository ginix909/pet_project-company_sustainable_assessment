# Generated by Django 4.0.1 on 2022-06-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0008_alter_indicators_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinstance',
            name='company_age',
            field=models.IntegerField(blank=True, null=True, verbose_name='Возраст компании'),
        ),
    ]

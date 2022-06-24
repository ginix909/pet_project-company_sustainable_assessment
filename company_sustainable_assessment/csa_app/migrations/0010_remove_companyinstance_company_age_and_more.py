# Generated by Django 4.0.1 on 2022-06-15 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0009_alter_companyinstance_company_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyinstance',
            name='company_age',
        ),
        migrations.AddField(
            model_name='companyinstance',
            name='year_of_analysis',
            field=models.IntegerField(blank=True, null=True, verbose_name='Календарный год для анализа'),
        ),
    ]

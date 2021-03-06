# Generated by Django 4.0.1 on 2022-06-17 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csa_app', '0011_indicators_indicator_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinstance',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='companyinstance',
            name='company_sector',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='Сектор промышленности'),
        ),
        migrations.AlterField(
            model_name='companyinstance',
            name='legal_form',
            field=models.CharField(default='', max_length=70, verbose_name='Орг.-правовая форма'),
        ),
    ]

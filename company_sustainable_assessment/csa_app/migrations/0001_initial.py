# Generated by Django 4.0.1 on 2022-05-13 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=70, verbose_name='Название')),
                ('company_sector', models.CharField(max_length=70, verbose_name='Сектор промышленности')),
                ('legal_form', models.CharField(max_length=70, verbose_name='Орг.-правовая форма')),
                ('company_age', models.IntegerField(blank=True, verbose_name='Возраст компании')),
                ('recording_date', models.DateField(default='2000-01-01', verbose_name='Дата записи')),
            ],
            options={
                'verbose_name': 'Запись в БД',
                'verbose_name_plural': 'Записи в БД',
            },
        ),
        migrations.CreateModel(
            name='Project_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=20)),
                ('relevance', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('goals', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
            ],
        ),
    ]

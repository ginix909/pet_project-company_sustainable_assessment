from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Project_info(models.Model): #я не использую эту БД. хотел так тупо вывести инфу о проекте.
    project_name = models.CharField(max_length=20)
    relevance = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    goals = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self): #вывод query set (коллекция записей класса (таблицы))
            return f'{self.project_name} - {self.author}%'

class CompanyInstance(models.Model):
    company_name = models.CharField('Название', max_length=70 )
    company_sector = models.CharField('Сектор промышленности',max_length=70)
    legal_form = models.CharField('Орг.-правовая форма',max_length=70)
    company_age = models.IntegerField('Возраст компании',blank=True)
    recording_date = models.DateField('Дата записи', default = '2000-01-01')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Запись в БД'
        verbose_name_plural = 'Записи в БД'

class Indicators(models.Model):
    # number = models.IntegerField(null=True)
    indicator = models.CharField( max_length=255)
    question = models.CharField( max_length=400)
    points = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return (f'{self.indicator}: {self.question}:{self.points}-баллов')

    def get_absolute_url(self):
        '''вренет адрес на который пойдем когда нажмем кнопку сабмит при перезаписи данных в форму'''
        if self.id == 10:
            return '/csa/result_db'
        return f'/csa/{self.id+1}/update'


from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Project_info(models.Model):
    project_name = models.CharField(max_length=20)
    relevance = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    goals = models.CharField(max_length=100)
    author = models.CharField(max_length=100)


    def __str__(self): #вывод query set (коллекция записей класса (таблицы))
        return f'{self.project_name} - {self.author}%'

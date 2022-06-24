from django.db import models

class CompanyInstance(models.Model):
    company_name = models.CharField('Название', max_length=70, blank=True, default='' )
    company_sector = models.CharField('Сектор промышленности',max_length=70, blank=True, default='')
    legal_form = models.CharField('Орг.-правовая форма',max_length=70, default='')
    year_of_analysis = models.IntegerField('Календарный год для анализа',blank=True, null=True)

    def __str__(self):
        return (f'Название компании: {self.company_name}. Сектор: {self.company_sector}. '
                f'Анализируемый год: {self.year_of_analysis}')

    def get_absolute_url(self):
        '''вренет адрес на который пойдем когда нажмем кнопку сабмит при перезаписи данных в форму'''
        return f'/csa/{self.id}/update_company_info'

    class Meta:
        '''пожалуй единственный участок кода в проекте, который я не знаю зачем. но по-моему, он добавляет
        куда-то название вот эти. называет что-то, что в этом проекте не выводится..'''
        verbose_name = 'Запись в БД'
        verbose_name_plural = 'Записи в БД'

class Indicators(models.Model):
    indicator = models.CharField( max_length=500)
    question = models.CharField( max_length=500)
    points = models.IntegerField(null=True, blank=True)
    indicator_values = models.CharField(max_length=1000,blank=True)

    def __str__(self):
        return (f'{self.indicator}: {self.question}:{self.points}-баллов')

    def get_absolute_url(self):
        '''вренет адрес на который пойдем когда нажмем кнопку сабмит при перезаписи данных в форму'''
        if self.id == 43:
            return '/csa/result_db'
        return f'/csa/{self.id+1}/update'


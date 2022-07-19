'''
Services - Сервисы – функции или классы, в которые чаще всего передаются объекты моделей (models),
над которыми сервисы выполняют какие-то манипуляции в соответствии с бизнес требованиями приложения.
То есть здесь будет лежать бизнес логика.
'''

from django.db.models import Sum
from .models import CompanyInstance, Indicators
from .static.csa_app.statistic_for_analysis import sector_average,sector_max,group_of_companies

from django.shortcuts import redirect

def save_valid_form(request,FormClass, redirect_url, error):
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('redirect_url')
        else:
            error = 'Форма ошибочно заполнена'

def score_analitics():
    '''
    рассчет показателей раздела "Аналитика набранных баллов" на странице
    "Результаты анализа ваших показателей устойчивости компании".
    '''
    total_points = Indicators.objects.aggregate(Sum('points')) #вернет словарь {'points_sum': число}
    total_points = total_points['points__sum']
    points_max = 43*5
    company_max_points = len(Indicators.objects.values_list('points').exclude(points=0).exclude(points=None)) * 5
    return {
        'total_points':total_points,
        'points_max': points_max,
        'company_max_points': company_max_points,
    }

def index_responsibility():
    total_points = Indicators.objects.aggregate(Sum('points')) #вернет словарь {'points_sum': число}
    total_points = total_points['points__sum']
    company_max_points = len(Indicators.objects.values_list('points').exclude(points=0).exclude(points=None)) * 5
    individual_value = round(total_points/company_max_points,2)

    sector = CompanyInstance.objects.all()[0].company_sector
    year_of_analysis = CompanyInstance.objects.all()[0].year_of_analysis
    industry_average = sector_average[sector][str(year_of_analysis)]
    industry_max = sector_max[sector][str(year_of_analysis)]
    difference='равно среднеотраслевому'
    dif_value=0
    if individual_value>industry_average:
        dif_value=round(individual_value-industry_average,2)
        difference = 'выше среднеотраслевого на'
    elif individual_value<industry_average:
        dif_value=round(industry_average-individual_value,2)
        difference = 'ниже среднеотраслевого на'
    return {
        'individual_value': individual_value,
        'industry_average': industry_average,
        'year_of_analysis': year_of_analysis,
        'difference':difference,
        'dif_value':dif_value,
        'sector': sector,
        'industry_max': industry_max,
    }

def index_analysis_in_groups():
    total_points = Indicators.objects.aggregate(Sum('points')) #вернет словарь {'points_sum': число}
    total_points = total_points['points__sum']
    company_max_points = len(Indicators.objects.values_list('points').exclude(points=0).exclude(points=None)) * 5
    individual_value = round(total_points/company_max_points,2)
    company_group = ''
    if individual_value >= 0.75:
        company_group = 'A'
    elif 0.65 < individual_value <0.74:
        company_group= 'B+'
    elif 0.55 < individual_value <0.64:
        company_group= 'B'
    elif 0.45 < individual_value <0.54:
        company_group= 'C'
    elif 0 < individual_value <0.54:
        company_group= 'Без группы'
    companies_in_group = group_of_companies[company_group]
    return {
        'company_group': company_group,
        'companies_in_group':companies_in_group,
    }

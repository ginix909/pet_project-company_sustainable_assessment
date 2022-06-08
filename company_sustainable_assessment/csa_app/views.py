from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Project_info, CompanyInstance, Indicators
from .forms import CompanyInstanceForm, IndicatorsForm
from django.views.generic import UpdateView
import pandas as pd

def get_project_info(request):
    '''переводит на главную страницу, на которой лежит информация о проекте'''
    return render(request,'csa_app/main_page.html')

def indicatorsform_is_valid(request):
    return HttpResponse ('Форма IndicatorsForm валидна, Форма сохранена')

def parsing_csv(request):
    ''''вытаскиваем построково значения из .csv, помещаем их в новый лист подружив с соответсвующими названиями
    из БД Indicators, далее методом bulk_create() сохраняем массив(лист) в Базу данных. И выдает данные в виде массива'''
    df = pd.read_csv('csa_app/indicators.csv', sep=';')
    indicators = []
    for i in range(len(df)):
        indicators.append(
            Indicators(
            # number=df.iloc[i][0],
            indicator=df.iloc[i][0],
            question=df.iloc[i][1],
            points=df.iloc[i][2],
            )
        )

    return HttpResponse (Indicators.objects.bulk_create(indicators))

def create_form_in_views(request):
    '''
    Функция сначала создает форму на основе класса формы, и передает эти данные в .html,
    в котором обьявляется полученная форма. данные полученные формой попадают сюда же (если не передать в теге
    формы именованные аргумент action='' и не указать где будет обрабатываться данные формы.)
    Проверяется на метод POST/GET, данные на валидность, сохраняет данные в БД, перенапавляет куда то например.
    '''
    error = ''
    if request.method == 'POST':
    #значит данные отправляются из формы. так как там в методе указано post. и больше нигде нет пока такого метода.
        form = IndicatorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('indicatorsform_is_valid')
        else:
            error = 'Форма была не верной'

    form = IndicatorsForm()
    args={
        'form': form,
        'error': error,
    }
    return render(request,'csa_app/evaluate_indicators.html',context=args)

class IndicatorsUpdateView(UpdateView):
    '''
    1.показать данные из формы - функция во вьюс с передачей БД в контекст по адресу
    2.новая запись в БД по форме - это функция во вьюс по созданию формы по БД, валиднации, записи полной новой строки в БД'''
    '''
    3.Этот класс нужен чтобы показать запись в форме и тут же ее перезаписать!
    класс отрабатывает по url: indicators_update.
    берет запись, на которую указали (у нас юрл конфиг обращается к self.id), помещает ее из БД в класс формы (в форму)
    и в тот .html который мы здесь указали посылает запись из БД. В этом .html надо создать форму и она будет заполнена.
    Какие поля в форме создашь, такие и заполнит. После того как записал в моделях в БД создай функцию get_absolute_url
    и верни ей путь куда идти после перезаписи. Это своего рода админка. '''
    model = Indicators
    template_name = 'csa_app/evaluate_indicators.html'
    form_class = IndicatorsForm

def current_db(request):
    ''' вызывается по адресу 'csa/current_db/'
    возвращает текущий вид базы данных (индикаторы, вопросы, баллы) '''
    indicators_db = Indicators.objects.all()
    data={
        'data':indicators_db,
    }
    return render(request, 'csa_app/current_db.html', context=data)

def result_db(request):
    ''' вызывается по адресу 'csa/result_db/'
    возвращает всю БД после записи балла в последний индикатор '''
    indicators_db = Indicators.objects.all()
    data={
        'data':indicators_db,
    }
    return render(request, 'csa_app/result_db.html', context=data)

def analysis(request):
    '''переход с кнопки  "Перейти к анализу индикаторов" на странице 'csa/result_db'
    считает баллы по колонке points. считаете сколько колонок оценены в 0 баллов.
    считает сколько должно быть баллов максимум, фльтруя not None значения points.
    вычитает из усредненнго балла по топ компаниям ваш балл и и пишет его в новы столбец и т.д'''
    # not_evaluate = Indicators.objects.values_list('indicator','points').filter(points=0)
    not_evaluated = Indicators.objects.values_list('indicator').filter(points__isnull=True)
    evaluate = Indicators.objects.values_list('indicator','points').filter(points__isnull=False)
    zero_evaluated = Indicators.objects.values_list('indicator').filter(points=0)
    total_points = Indicators.objects.aggregate(Sum('points')) #вернет словарь {'points_sum': число}
    total_points = total_points['points__sum']
    points_max = 43*5                   #43 индикатора по 5 баллов максимум каждый
    company_max_points = len(evaluate) * 5                # n индикаторов, которые оценены (not None) * 5
    data = {
        'total_points': total_points,
        'points_max': points_max,
        'company_max_points': company_max_points,
        'not_evaluated': not_evaluated,
        'zero_evaluated': zero_evaluated,
    }
    return render(request, 'csa_app/analysis.html', context=data)

def not_evaluated(request):
    return HttpResponse ('Рекомендации по неоцененным параметрам')

def zero_evaluated(request):
    return HttpResponse ('Рекомендации по "нулевым" параметрам')

def empty_points(request):
    # new = Indicators.objects.filter(indicator='Ind').update(points=0)
    # Indicators.objects.get(indicator='Ind').update(points=0)
    Indicators.objects.all().update(points=None)
    # new = Indicators.objects.filter(indicator='Ind').delete()
    redirect_url = reverse('current_db')
    return HttpResponseRedirect(redirect_url)

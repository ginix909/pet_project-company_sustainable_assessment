from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import CompanyInstance, Indicators
from .forms import CompanyInstanceForm, IndicatorsForm
from django.views.generic import UpdateView
from .services import save_valid_form, score_analitics, index_responsibility, index_analysis_in_groups
from .static.csa_app.statistic_for_analysis import sector_average,sector_max,group_of_companies

def get_project_info(request):
    '''переводит на главную страницу, на которой лежит информация о проекте'''
    return render(request,'csa_app/main_page.html')

def indicatorsform_is_valid(request):
    '''
    сюда попадем, если юзер сделал запись в пользовательскую форму IndicatorsForm,
    но не указал куда переходить дальше.
    '''
    return HttpResponse ('Форма IndicatorsForm валидна, Форма сохранена')

def companyinstanceform_is_valid(request):
    '''
    сюда попадем, если юзер сделал запись в пользовательскую форму CompanyInstanceForm,
    но не указал куда переходить дальше
    '''
    return HttpResponse ('Форма CompanyInstanceForm валидна, Форма сохранена')


def company_info(request):
    '''
    Функция сначала создает форму на основе класса формы, и передает эти данные в .html,
    в котором объявляется полученная форма. данные полученные формой попадают сюда же (если не передать в теге
    формы именованные аргумент action='' и не указать где будет обрабатываться данные формы.)
    Проверяется на метод POST/GET, данные на валидность, сохраняет данные в БД, перенапавляет куда то например.
    '''
    error = ''
    save_valid_form(request,CompanyInstanceForm,'companyinstanceform_is_valid',error)

    form = CompanyInstanceForm()
    args={
        'form': form,
        'error': error,
    }
    return render(request,'csa_app/company_info.html',context=args)

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
    Наследуется от свтроенного класса UpdateView.
    Этот класс нужен чтобы показать запись в форме и тут же ее перезаписать! класс отрабатывает по url: indicators_update.
    берет запись, на которую указали (у нас юрл конфиг обращается к self.id), помещает ее из БД в класс формы (в форму)
    и в тот .html который мы здесь указали посылает запись из БД. В этом .html надо создать форму и она будет заполнена.
    Какие поля в форме создашь, такие и заполнит. После того как записал в моделях в БД создай функцию get_absolute_url
    и верни ей путь куда идти после перезаписи. '''
    model = Indicators
    template_name = 'csa_app/evaluate_indicators.html'
    form_class = IndicatorsForm

class CompanyInstanceUpdateView(UpdateView):
    '''
    Наследуется от встроенного класса UpdateView.
    Этот класс нужен чтобы показать запись в форме и тут же ее перезаписать! класс отрабатывает по url: company_instance_update.
    берет запись, на которую указали (у нас юрл конфиг обращается к self.id), помещает ее из БД в класс формы (в форму)
    и в тот .html который мы здесь указали посылает запись из БД. В этом .html надо создать форму и она будет заполнена.
    Какие поля в форме создашь, такие и заполнит. После того как записал в моделях в БД создай функцию get_absolute_url
    и верни ей путь куда идти после перезаписи. Это своего рода админка. '''
    model = CompanyInstance
    template_name = 'csa_app/company_info.html'
    form_class = CompanyInstanceForm

def current_db(request):
    ''' вызывается по адресу 'csa/current_db/'
    возвращает текущий вид базы данных (индикаторы, вопросы, баллы) '''
    indicators_db = Indicators.objects.all()
    company_info = CompanyInstance.objects.all()
    data={
        'data':indicators_db,
        'company_info': company_info,
    }
    return render(request, 'csa_app/current_db.html', context=data)

def result_db(request):
    ''' вызывается по адресу 'csa/result_db/'
    возвращает всю БД после записи балла в последний индикатор '''
    indicators_db = Indicators.objects.all()
    evaluate = Indicators.objects.values_list('points').exclude(points=0).exclude(points=None)
    if evaluate:
        data={
            'data':indicators_db,
        }
        return render(request, 'csa_app/result_db.html', context=data)
    else:
        return HttpResponse ("Вы не оценили ни одного показателя")

def analysis(request):
    '''переход с кнопки  "Перейти к анализу индикаторов" на странице 'csa/result_db'
    считает баллы по колонке points. считаете сколько колонок оценены в 0 баллов.
    считает сколько должно быть баллов максимум, фльтруя not None значения points.
    вычитает из усредненнго балла по топ компаниям ваш балл и пишет его в новы столбец и т.д
    вызывает функции расчета групп показателей, из файла services.py
    Можно сделать для каждой группы view, если бы они показывались не всегда вместе.
    чтобы они вызывались отдельно, чтобы каждый показатель расчитывался по мере вызова.'''
    evaluate = Indicators.objects.values_list('points').exclude(points=0).exclude(points=None)
    if evaluate:
        not_evaluated = Indicators.objects.values_list('indicator', flat=True).filter(points__isnull=True)
        zero_evaluated = Indicators.objects.values_list('indicator', flat=True).filter(points=0)

        data = {
            'not_evaluated': not_evaluated,
            'zero_evaluated': zero_evaluated,
        }
        data.update(score_analitics())
        data.update(index_responsibility())
        data.update(index_analysis_in_groups())
        return render(request, 'csa_app/analysis.html', context=data)
    else:
        return HttpResponse ("Вы еще не оценивали показатели. Вернитесь назад.")


def not_evaluated(request):
    '''Переход с кнопки "рекомендации по неоцинаваемым индикаторам".
    Покажет в чем ценность раскрытия данной группы индикаторов (если были неоцениваемые индикаторы)'''
    not_evaluated = Indicators.objects.values_list ('indicator', 'indicator_values').filter (points__isnull=True)
    data = {
        'not_evaluated': not_evaluated,
    }
    return render (request, 'csa_app/not_evaluated.html', context=data)

def empty_points(request):
    '''Очистить все оценки, которые пользователь ввел. Если нужно оценить другую компанию, другой год, перезаписать.'''
    Indicators.objects.all().update(points=None)
    redirect_url = reverse('current_db')
    return HttpResponseRedirect(redirect_url)

def prospects(request):
    '''отправляет на страницу с информацией о перспективах развития проекта'''
    return render(request, 'csa_app/prospects.html')

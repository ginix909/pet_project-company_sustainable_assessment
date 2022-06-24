from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import CompanyInstance, Indicators
from .forms import CompanyInstanceForm, IndicatorsForm
from django.views.generic import UpdateView

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
    в котором обьявляется полученная форма. данные полученные формой попадают сюда же (если не передать в теге
    формы именованные аргумент action='' и не указать где будет обрабатываться данные формы.)
    Проверяется на метод POST/GET, данные на валидность, сохраняет данные в БД, перенапавляет куда то например.
    '''
    error = ''
    if request.method == 'POST':
    #значит данные отправляются из формы. так как там в методе указано post. и больше нигде нет пока такого метода.
        form = CompanyInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companyinstanceform_is_valid')
        else:
            error = 'Форма была не верной'

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

sector_average = {
    'Электроэнергетика':{'2021':0.78,'2020':0.10},
    'Нефтяная промышленность':{'2021':0.75,'2020':0.10},
}
sector_max = {
    'Электроэнергетика':{'2021':0.82,'2020':0.10},
    'Нефтяная промышленность':{'2021':0.94,'2020':0.10},
}
group_of_companies = {
    'A':'Алроса, АФК Система, Газпром, Интер РАО...21 компания',
    'B+':'Вымпелком, Камаз, ЛСР...12 компаний',
    'B':'X5 Retail Group, Аэрофлот, ВТБ, Газпромбанк...15 компаний',
    'C':'ВЭБ.РФ, Детский мир, Русагро, Сургутнефтегаз',
    'Без группы': 'Ваша компания показала очень низкое индивидуальное значение индекса и не вошла ни в одну группу',
}
def analysis(request):
    '''переход с кнопки  "Перейти к анализу индикаторов" на странице 'csa/result_db'
    считает баллы по колонке points. считаете сколько колонок оценены в 0 баллов.
    считает сколько должно быть баллов максимум, фльтруя not None значения points.
    вычитает из усредненнго балла по топ компаниям ваш балл и и пишет его в новы столбец и т.д'''
    # not_evaluate = Indicators.objects.values_list('indicator','points').filter(points=0)
    evaluate = Indicators.objects.values_list('points').exclude(points=0).exclude(points=None)
    if evaluate:
        not_evaluated = Indicators.objects.values_list('indicator').filter(points__isnull=True)
        not_evaluated = [x[0] for x in not_evaluated]
        evaluate = Indicators.objects.values_list('indicator','points').filter(points__isnull=False)
        zero_evaluated = Indicators.objects.values_list('indicator').filter(points=0)
        zero_evaluated = [x[0] for x in zero_evaluated]
        total_points = Indicators.objects.aggregate(Sum('points')) #вернет словарь {'points_sum': число}
        total_points = total_points['points__sum']
        points_max = 43*5                   #43 индикатора по 5 баллов максимум каждый
        company_max_points = len(evaluate) * 5                # n индикаторов, которые оценены (not None) * 5

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
        sector = CompanyInstance.objects.all()[0].company_sector
        year_of_analysis = CompanyInstance.objects.all()[0].year_of_analysis
        companies_in_group = group_of_companies[company_group]
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
        data = {
            'total_points': total_points,
            'points_max': points_max,
            'company_max_points': company_max_points,
            'not_evaluated': not_evaluated,
            'zero_evaluated': zero_evaluated,
            'individual_value': individual_value,
            'company_group': company_group,
            'industry_average': industry_average,
            'year_of_analysis': year_of_analysis,
            'difference':difference,
            'dif_value':dif_value,
            'sector': sector,
            'industry_max': industry_max,
            'companies_in_group':companies_in_group,
        }
        return render(request, 'csa_app/analysis.html', context=data)
    else:
        return HttpResponse ("Вы еще не оценивали показатели. Вернитесь назад.")
def not_evaluated(request):
    '''Переход с кнопки "рекомендации по неоцинаваемым индикаторам".
    Покажет в чем ценность раскрытия данной группы индикаторов (если были неоцениваемые индикаторы)'''
    not_evaluated = Indicators.objects.values_list('indicator','indicator_values').filter(points__isnull=True)
    not_evaluated = [ (x[0],x[1]) for x in not_evaluated]
    data={
        'not_evaluated': not_evaluated,
    }
    return render(request, 'csa_app/not_evaluated.html', context=data)

def empty_points(request):
    '''Очистить все оценки, которые пользователь ввел. Если нужно оценить другую компанию, другой год, перезаписать.'''
    Indicators.objects.all().update(points=None)
    redirect_url = reverse('current_db')
    return HttpResponseRedirect(redirect_url)

def prospects(request):
    '''отправляет на страницу с информацией о перспективах развития проекта'''
    return render(request, 'csa_app/prospects.html')



# def zero_evaluated(request):
#     return HttpResponse ('Рекомендации по "нулевым" параметрам')

# def parsing_csv(request):
#     ''''вытаскиваем построково значения из .csv, помещаем их в новый лист подружив с соответсвующими названиями
#     из БД Indicators, далее методом bulk_create() сохраняем массив(лист) в Базу данных. И выдает данные в виде массива'''
#     df = pd.read_csv('csa_app/indicators.csv', sep=';')
#     indicators = []
#     for i in range(len(df)):
#         indicators.append(
#             Indicators(
#             indicator=df.iloc[i][0],
#             question=df.iloc[i][1],
#             points=df.iloc[i][2],
#             )
#         )
#
#     return HttpResponse (Indicators.objects.bulk_create(indicators))

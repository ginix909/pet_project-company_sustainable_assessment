from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project_info, CompanyInstance
from .forms import CompanyInstanceForm

def get_project_info(request):
    '''представление выведет информацию по проекту, которая лжежит в БД, которая описана в models.py'''
    # project_info = Project_info
    # return HttpResponse(project_info)
    return render(request,'csa_app/main_page.html')

# def create_form_in_views(request):
#     '''функция для передачи формы модели в шаблон html длы создания html формы'''
#     form = CompanyInstanceForm()
#     args={'form': form}
#     return render(request,'csa_app/evaluate_company.html',context = args)


def create_form_in_views(request):
    '''
    Функция .....
    функция для передачи формы модели в шаблон html длы создания html формы'''
    error = ''
    if request.method == 'POST':
    #значит данные отправляются из формы. так как там в методе указано post. и больше нигде нет пока такого метода.
        form = CompanyInstanceForm(request.POST)
        #request.POST вставляет данные от пользователя в форму, которая привязана к модели БД
        if form.is_valid(): #теперь проверяем корректно ли данные заполнились в форму.
        # проверять будет по указанным типам в форме или в модели (думаю в модели)
            form.save()
            return redirect('analysis_result')
        else:
            error = 'Форма была не верной'

    form = CompanyInstanceForm()
    args={
        'form': form,
        'error': error
    }
    return render(request,'csa_app/evaluate_company.html',context = args)

def analysis_result(request):
    return HttpResponse ('Форма сохранена')

import pandas as pd
from .models import Indicators

def show_csv(request):
    df = pd.read_csv('indicators2.csv', sep='delimiter')
    indicators = []
    for i in range(len(df)):
        indicators.append(
            Indicators(
            number=df.iloc[i][0],
            indicator=df.iloc[i][1],
            question=df.iloc[i][2],
            points=df.iloc[i][3],
            )
        )

    return HttpResponse (Indicators.objects.bulk_create(indicators))

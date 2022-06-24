from django.urls import path, include
from . import views as csa_app_views

urlpatterns = [
    path('', csa_app_views.get_project_info, name = 'csa_app_main' ),
    path('company_info/', csa_app_views.company_info, name='company_info'),
    path('<int:pk>/update/', csa_app_views.IndicatorsUpdateView.as_view(), name='indicators_update'),
    path('<int:pk>/update_company_info/', csa_app_views.CompanyInstanceUpdateView.as_view(), name='company_instance_update'),
    path('current_db/', csa_app_views.current_db, name='current_db'),
    path('result_db/', csa_app_views.result_db, name='result_db'),
    path('result_db/analysis/', csa_app_views.analysis, name='analysis'),
    path('result_db/analysis/not_evaluated', csa_app_views.not_evaluated, name='not_evaluated'),
    path('current_db/deleting', csa_app_views.empty_points, name='empty_points'),
    path('prospects', csa_app_views.prospects, name='prospects'),
    # path('create/', csa_app_views.create_form_in_views, name='create_form_in_views'),
    # path('create/indicatorsform_is_valid/', csa_app_views.indicatorsform_is_valid, name='indicatorsform_is_valid'),
    # path('create/companyinstanceform_is_valid/', csa_app_views.companyinstanceform_is_valid, name='companyinstanceform_is_valid'),
    # path('create/show_csv/', csa_app_views.parsing_csv, name='show_csv'),
    # path('result_db/analysis/zero_evaluated', csa_app_views.zero_evaluated, name='zero_evaluated'),
]

'''
Путь пользователя по URL-config приложения csa_app внутри проекта company_sustainable_assessment.
шаг 0. ''               главная страница. пользователь попадает сюда автоматически и видит общую инормацию о проекте.
                        далее предполагается что юзер обратиться к контекстному меню слева. там предполагается что он
                        пойдет именно по следующему алгоритму.
                        
шаг 1.                  юзер нажимает на кнопку "ввести общую информацию о компании",заполняет пользовательскую форму
                        если не заполнит - в конце получит не корректный анализ - по этому нужно будет поместить этот
                        этап в кнопку "оценить компанию"
                        
шаг 2. 1/update/        юзер нажимает кнопку "Оценить компанию" переходим в динамический url, в который сразу 
                        получаем 1 в качестве self.id - первого индикатора нашей оценочной базы. Юзер оценивает 
                        индикаторы устойчивости по своей компании. При каждом нажатии "Записать оценку индикатора"
                        данное поле формы сохраняется и переводит нас на след индикатор. счетчик индикаторов в 
                        models.py, class Indicators, функция get_absolute_url().

шаг 3. result_db/       попадаем после оценки последнего индикатора, при условии что дошли до индикатора с id = 43.
                        так как у нас 43 индикатора. записано в models.py, class Indicators, функция get_absolute_url().

шаг 4 result_db/analysis/ попали по кнопке "перейти к анализу индикаторов". Здесь показвается сводный анализ по 
                        оцененным индикаторам. далее юзер может пойти по углубленному анализу разных направлений.

шаги на выбор, не влияющие на корректность конечных результатов:

current_db/             посмотреть текущую базу данных - покажет информацию, которую мы записали на данный момент. 
                        что оценили. Какую общую информацию указали. Может пригодится и в конце, чтобы вспомнить оценки.
                        
prospects/              из главного меню - информация о перспективах проекта.

result_db/analysis/     из главного меню перейти сразу к аналитике. там будут пустые поля или пару оценок, которые 
                        оставил юзер.
                        
                        из главного меню "оценить свои знания в области УР"
                        внешняя сслыка на разработанный тест о ваших знаниях по устойчивому развитию.

                        из главного меню "Устойчивое развитие это" достоверный источник справочной информации по 
                        предмету Устойчивого развития.
                        
задокументированные url-config-и ссылаются на использованную и, возможно, полезную в будущем функциональность,
такую как загрузка и парсинг файла с индикаторами, вопросами и ценностью, 
создание индикаторов юзером,
аналитика по "нулевым индикаторам"

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 - это мой токен на гите.. я не знаю куда его положить.
'''


'''
Можно доделать, но автор не знает как:
1. защитить от перезаписи поле индикатор и вопрос
2. кнопка предыдущий вопрос
3. поменять в forms.py class CompanyInstanceForm тип поля legal_form на ChoiceField. но не через виджеты, а отдельным 
объявление поля (явно свалиться отображение в html, но скорее всего там в аргументы можно будет передать и attrs{}.
я попробовал так сделать но у меня поле не отображается. может родительский класс нужно будет поменять на forms.Form
'''

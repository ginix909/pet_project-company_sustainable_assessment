from django.urls import path, include
from . import views as csa_app_views

urlpatterns = [
    path('', csa_app_views.get_project_info, name = 'csa_app_main' ),
    path('create/', csa_app_views.create_form_in_views, name='create_form_in_views'),
    path('create/indicatorsform_is_valid/', csa_app_views.indicatorsform_is_valid, name='indicatorsform_is_valid'),
    path('create/show_csv/', csa_app_views.parsing_csv, name='show_csv'),
    path('<int:pk>/update/', csa_app_views.IndicatorsUpdateView.as_view(), name='indicators_update'),
    path('current_db/', csa_app_views.current_db, name='current_db'),
    path('result_db/', csa_app_views.result_db, name='result_db'),
    path('result_db/analysis/', csa_app_views.analysis, name='analysis'),
    path('result_db/analysis/not_evaluated', csa_app_views.not_evaluated, name='not_evaluated'),
    path('result_db/analysis/zero_evaluated', csa_app_views.zero_evaluated, name='zero_evaluated'),
    path('current_db/deleting', csa_app_views.empty_points, name='empty_points'),

]

'''
1. ''                         главная страница
2. 1/update/                  попадаем сюда после нажатия кнопки Оценить компанию, получаем сразу адрес 1/update
                              Это начало и транизитный путь после начала прохождения опроса, перенаправляет на след вопрос
.                            покажет проанализированные данные
3. create/                    в нашем случае выводит форму для перезаписи данных 
                              (из другой вью мы заполняем ее данными), также проходит валидация новых данны.
3.1                           конпка записать данные формирует ссылку на след индикатор, так мы проходим их все.
4. result_db/                 cтраница с инидкаторами и баллами. заполненная БД.
5. analysis/                 страница где показан анализ данных

изначально в поле points стоит null. Кнопка "не оценивать" ставит туда пустую строку. Дальше проверяется по условию
__isnull=True. И достигается эффект не оцененности поля.
create/indicatorsform_is_valid/ текущая проверка валидности формы. в конце можно добавить что типо данные сохранены.
create/show_csv/                парсит файл csv c индикаторами. в конце эту кнопку нужно будет убрать.

'''

'''
-заходим на сайт. Простые ссылки визуализации:почитать теорию, пройти тест, ознакомиться с индикаторами, с методикой)
- путь оценки устойчивости компании по индикаторам:
-нажимае оценить компанию (показывается форма из БД с индикатороами и вопросами)
-отвечаем на вопросы по своей компании, тем самым присваиваем баллы по каждому индикатору.
-видим общую таблицу с вопросами и баллами. Если что-то не устраивает-нажимаем оценить компанию и снова проходим 
по всем вопросам. - слабое место. нужно добавить кнопку посмотреть результат на все страницы. кнопка есть.
- нажимаем на кнопку "перейти к анализу индикаторов". знакомимся с данными анализа.
'''

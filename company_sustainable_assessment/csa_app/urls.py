from django.urls import path, include
from . import views as csa_app_views

urlpatterns = [
    path('', csa_app_views.get_project_info, name = 'csa_app_main' ),
    # path('Evaluate_company', csa_app_views.evaluate_company, name='evaluate_company'),
    #Оценить компанию" это префикс,
    # по которому мы будем обращаться к функции evaluate_company (которую мы уже создали во views),
    # а она в свою очередь будет возвращать нам шаблон страницы evaluate_company.html.
    path('create/', csa_app_views.create_form_in_views, name='create_form_in_views'),
    path('create/analysis_result/', csa_app_views.analysis_result, name='analysis_result'),
    path('create/show_csv/', csa_app_views.show_csv, name='show_csv'),

]



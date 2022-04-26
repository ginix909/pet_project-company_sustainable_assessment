from django.urls import path, include
from . import views as csa_app_views

urlpatterns = [
    path('', csa_app_views.get_project_info ),
    # path('Evaluate_company', csa_app_views.evaluate_company, name='evaluate_company'),
    #Оценить компанию" это префикс,
    # по которому мы будем обращаться к функции evaluate_company (которую мы уже создали во views),
    # а она в свою очередь будет возвращать нам шаблон страницы evaluate_company.html.
    path('evaluate_company/', csa_app_views.evaluate_company, name='evaluate_company'),
]



from django.urls import path, include
from . import views as csa_app_views

urlpatterns = [
    path('', csa_app_views.get_project_info ),

]



from django.contrib import admin
from .models import Indicators

# admin.site.register(Indicators) - можно так зарегистрировать в админке класс

@admin.register(Indicators)
class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ['indicator','question','points']

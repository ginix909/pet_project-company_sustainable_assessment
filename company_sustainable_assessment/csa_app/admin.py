from django.contrib import admin
from .models import Project_info, Indicators

admin.site.register(Project_info)

@admin.register(Indicators)
class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ['indicator','question','points']

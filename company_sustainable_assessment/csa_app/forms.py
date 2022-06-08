from django.forms import ModelForm, TextInput, DateInput, NumberInput
from .models import CompanyInstance, Indicators

class CompanyInstanceForm(ModelForm): #создали форму, которая привязана к модели
    class Meta: #позволяет описать некие реквизиты модели
        model = CompanyInstance
        fields = '__all__'
        # fields = ['company_name', 'company_sector']
        widgets= {
            'company_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название компании'
            }),
            'company_sector': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сектор'
            }),
            'legal_form': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ОПФ'
            }),
            'company_age': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Возраст'
            }),
            'recording_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата записи'
            })
        }

class IndicatorsForm(ModelForm):
    '''создаем форму БД Indicators. В ней данные из indicators.csv. мы достанем оттуда записи из полей indicator,
    question и будем выводить их по очереди вместе с вариантами ответа.
    потом во views обработаем и запишем полученные данные( баллы points) в БД Indicators'''
    class Meta():
        model = Indicators
        fields = ['indicator','question','points']
        widgets= {
            'indicator': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Индикатор'
            }),
            'question': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вопрос'
            }),
            'points': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Баллы'
            }),
        }

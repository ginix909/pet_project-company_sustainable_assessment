from django.forms import ModelForm, TextInput, NumberInput, Textarea, ChoiceField
from .models import CompanyInstance, Indicators
from django import forms

legal_forms_list= {
    ('АО','Акционерное общество'),
    ('ПАО','Публичное акционерное общество'),
    ('НАО','Непубличное акционерное общество'),
    ('НКО','Некоммерческая организация'),
}
class CompanyInstanceForm(ModelForm): #создали форму, которая привязана к модели
    class Meta: #позволяет описать некие реквизиты модели
        model = CompanyInstance
        # fields = '__all__'
        fields = ['company_name', 'company_sector','legal_form','year_of_analysis']
        # legal_form = forms.ChoiceField(choices=legal_forms_list)
        widgets= {
            'company_name': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Название компании',
                'cols': 50,
                'rows': 2,
            }),
            'company_sector': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Сектор',
                'cols': 50,
                'rows':1,
            }),
            'legal_form': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'ОПФ',
                'cols': 50,
                'rows':1,
            }),
            'year_of_analysis': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анализируемый год',
                'cols': 50,
            }),
        }

class IndicatorsForm(ModelForm):
    '''создаем форму БД Indicators. В ней данные из indicators.csv. мы достанем оттуда записи из полей indicator,
    question и будем выводить их по очереди вместе с вариантами ответа.
    потом во views обработаем и запишем полученные данные( баллы points) в БД Indicators'''
    class Meta():
        model = Indicators
        fields = ['indicator','question','points']
        widgets= {
            'indicator': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Индикатор',
                'rows': 2,
                'cols': 80,
            }),
            'question': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Вопрос',
                'rows': 2,
                'cols':80,
            }),
            'points': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Баллы'
            }),
        }

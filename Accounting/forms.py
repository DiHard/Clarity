from .models import Organization, Dogovor
from django.forms import ModelForm, TextInput, Textarea


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['full_name', 'short_name', 'inn', 'kpp', 'ur_adres', 'management_full_name', 'management_post']
        widgets = {
            'full_name': TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Общество с ограниченной ответственностью "Полное наименование организации"'
            }),
            'short_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ООО "ПНО"'
            }),
            'inn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0000000000'
            }),
            'kpp': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000000000'
            }),
            'ur_adres': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '443322, г. Город, ул. Улица, дом 99, офис 99'
            }),
            'management_full_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия Имя Отчество'
            }),
            'management_post': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Генеральный директор'
            })
        }


class DogovorForm(ModelForm):
    class Meta:
        model = Dogovor
        fields = ['nomer_dogovora']
        widgets = {'nomer_dogovora': TextInput(attrs={
            'class': 'from-control',
            'placeholder': 'Введите название'
        })
        }
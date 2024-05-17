from .models import Organization, Dogovor, Service
from django.forms import ModelForm, TextInput, DateInput, URLInput, CheckboxInput, Select


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
        fields = ['nomer_dogovora', 'date_of_signing', 'web_site', 'contract_completed', 'basic_price', 'service_type', 'organization']
        widgets = {
            'nomer_dogovora': TextInput(attrs={
                'class': 'form-control'
                }),
            'date_of_signing': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'dd.mm.yyyy'
                }),
            'web_site': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'site.ru'
                }),
            'contract_completed': CheckboxInput(attrs={
                'class': "form-check-input",
                'type': "checkbox",
                'role': "switch"
                }),
            'basic_price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
                }),
            'service_type': Select(attrs={
                'class': 'form-select'
                }),
            'organization': Select(attrs={
                'class': 'form-select'
                })

        }


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'date_start', 'date_end', 'price', 'payment_made', 'dogovor', 'full_payment', 'act_approved']
        widgets = {
            'service_name': TextInput(attrs={
                'class': 'form-control'
                }),
            'date_start': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'dd.mm.yyyy'
                }),
            'date_end': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'dd.mm.yyyy'
                }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
                }),
            'payment_made': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
                }),
            'dogovor': Select(attrs={
                'class': 'form-select'
                }),
            'full_payment': CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox'
                }),
            'act_approved': CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox'
                })
        }

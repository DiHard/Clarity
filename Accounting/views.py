from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import OrganizationForm, DogovorForm
from .generate import generate, translit

from .models import Organization, Dogovor, Service


def dashboard(request):
    organization_list = Organization.objects.all()
    dogovor_list = Dogovor.objects.all()
    service_list = Service.objects.all()
    return render(request, 'Accounting/dashboard.html',
                  {'title': 'Сводка', 'organization_list': organization_list,
                   'dogovor_list': dogovor_list, 'service_list': service_list})


# Create your views here.
def index(request):
    organization_list = Organization.objects.all()
    dogovor_list = Dogovor.objects.all()
    service_list = Service.objects.all()
    return render(request, 'Accounting/index.html',
                  {'title': 'Главная страница сайта', 'organization_list': organization_list,
                   'dogovor_list': dogovor_list, 'service_list': service_list})





def about(request):
    print("Так можно! Просто функция в представлении!")

    return render(request, 'Accounting/about.html')


def organization_detail(request, pk):
    # Функция запускает детальную страницу Организации
    organization_list = Organization.objects.get(
        id=pk)  # создаем список, который содержит данные организации по переданному ID
    dogovor_list = Dogovor.objects.filter(
        organization=organization_list)  # Создаем список всех договоров организации
    service_list = Service.objects.filter(dogovor__in=dogovor_list)
    return render(request, 'Accounting/organization-detail.html',
                  {'organization_list': organization_list, 'dogovor_list': dogovor_list,
                   'service_list': service_list})

def organization_edit(request, pk):
    # Редактирование договора
    organization = Organization.objects.get(id=pk)
    error = ''
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization-detail', pk=pk)
        else:
            error = 'Произошла ошибка сохранения: форма содержала некоректные данные'
    form = OrganizationForm(instance=organization)
    context = {
        'form': form,
        'organization': organization,
        'error': error
    }
    return render(request, 'Accounting/organization-edit.html', context)

def organization_create(request):
    error = ''
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = OrganizationForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'Accounting/organization-create.html', context)

def dogovor_detail(request, pk):
    # Функция запускает детальную страницу Договра
    dogovor_list = Dogovor.objects.get(id=pk)
    return render(request, 'Accounting/dogovor-detail.html', {'dogovor_list': dogovor_list})


def dogovor_edit(request, pk):
    # Редактирование договора
    dogovor = Dogovor.objects.get(id=pk)
    error = ''
    if request.method == 'POST':
        form = DogovorForm(request.POST, instance=dogovor)
        if form.is_valid():
            form.save()
            return redirect('dogovor-detail', pk=pk)
        else:
            error = 'Форма была неверной'
    form = DogovorForm(instance=dogovor)
    form.nomer_dogovora = dogovor.nomer_dogovora  # Это определяет какими значениями будет предзаполнена форма при загрузке
    context = {
        'form': form,
        'dogovor': dogovor,
        'error': error
    }
    return render(request, 'Accounting/dogovor-edit.html', context)




def dogovor_generate(request, pk):
    dogovor_list = Dogovor.objects.get(id=pk)
    generate(dogovor_list)

    # Блок - Скачиваем файл в браузере
    # Генерируем имя конечного файла
    file_name = translit(
        dogovor_list.nomer_dogovora)  # Переводим в транслит, тк с кириллицей проблемы.
    # Создайте объект HttpResponse, чтобы отправить файл в браузер
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f"attachment; filename={file_name}.docx"

    # Откройте созданный файл и запишите его содержимое в ответ
    with open("static/Generate/generated.docx", "rb") as f:
        response.write(f.read())

    return response


def service_detail(request, pk):
    # Функция запускает детальную страницу Услуги
    service_list = Service.objects.get(id=pk)
    return render(request, 'Accounting/service-detail.html', {'service_list': service_list})

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import F
from .forms import OrganizationForm, DogovorForm, ServiceForm
from .generate import generate, translit, period

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
    # создаем список, который содержит данные организации по переданному ID
    organization_list = Organization.objects.get(id=pk)
    # Создаем список всех договоров организации
    dogovor_list = Dogovor.objects.filter(organization=organization_list)
    # Создаем список всех услуг организации
    service_list = Service.objects.filter(dogovor__in=dogovor_list)

    # Добавляем в список услгу расчет задолженности
    for el in service_list:
        el.debt = el.price - el.payment_made
    # Добавляем в список услгу расчет периода
    for el in service_list:
        el.period = (el.date_end - el.date_start).days + 1


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
    service_list = Service.objects.filter(dogovor=dogovor_list)
    context = {
        'dogovor_list': dogovor_list,
        'service_list': service_list
    }
    return render(request, 'Accounting/dogovor-detail.html', context)


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
    context = {
        'form': form,
        'dogovor': dogovor,
        'error': error
    }
    return render(request, 'Accounting/dogovor-edit.html', context)



def dogovor_create(request):
    error = ''
    if request.method == 'POST':
        form = DogovorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = DogovorForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'Accounting/dogovor-create.html', context)

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
    # Считаем сколько дней период между датами
    service_list.period = (service_list.date_end - service_list.date_start).days + 1
    # Считаем остаток задолжености
    service_list.debt = service_list.price - service_list.payment_made
    return render(request, 'Accounting/service-detail.html', {'service_list': service_list})


def service_edit(request, pk):
    # Редактирование договора
    service = Service.objects.get(id=pk)
    error = ''
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service-detail', pk=pk)
        else:
            error = 'Форма была неверной'
    form = ServiceForm(instance=service)
    context = {
        'form': form,
        'service': service,
        'error': error
    }
    return render(request, 'Accounting/service-edit.html', context)


def service_create(request):
    error = ''
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = ServiceForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'Accounting/service-create.html', context)
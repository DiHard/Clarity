from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import OrganizationForm, DogovorForm, ServiceForm
from .generate import generate, translit, generate_bill, generate_act
from dadata import Dadata # pip install dadata
from .models import Organization, Dogovor, Service
import datetime

@login_required
def dashboard(request):
    organization_list = Organization.objects.all()
    dogovor_list = Dogovor.objects.all()
    service_list = Service.objects.all()
    # Добавляем в список услгу расчет периода
    for el in service_list:
        el.period = (el.date_end - el.date_start).days + 1
    # Добавляем в список услгу расчет задолженности
    for el in service_list:
        el.debt = el.price - el.payment_made
    content = {
        'organization_list': organization_list,
        'dogovor_list': dogovor_list,
        'service_list': service_list
    }
    return render(request, 'Accounting/dashboard.html', content)

@login_required
def organizations(request):
    organization_list = Organization.objects.all()
    dogovor_list = Dogovor.objects.all()
    service_list = Service.objects.all()
    # Добавляем в список услгу расчет периода
    for el in service_list:
        el.period = (el.date_end - el.date_start).days + 1
    # Добавляем в список услгу расчет задолженности
    for el in organization_list:
        el.doc_count = Dogovor.objects.filter(organization=el.id).count()
    content = {
        'organization_list': organization_list,
        'dogovor_list': dogovor_list,
        'service_list': service_list
    }
    return render(request, 'Accounting/organizations.html', content)


@login_required
def index(request):
    organization_list = Organization.objects.all().order_by('-id')[:4]
    dogovor_list = Dogovor.objects.all().order_by('-id')[:4]
    service_list = Service.objects.all()
    content = {
        'title': 'Главная страница сайта',
        'organization_list': organization_list,
        'dogovor_list': dogovor_list,
        'service_list': service_list
    }
    return render(request, 'Accounting/index.html', content)

@login_required
def about(request):
    print("Это вторая ветка")
    return render(request, 'Accounting/about.html')

@login_required
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
    # Считаем задолженность по договору
    for el in service_list:
        el.period = (el.date_end - el.date_start).days + 1


    return render(request, 'Accounting/organization-detail.html',
                  {'organization_list': organization_list, 'dogovor_list': dogovor_list,
                   'service_list': service_list})

@login_required
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

@login_required
def organization_create_by_inn(request, pk):
    # Добавление организации по id
    dadata = Dadata('0fc7d60da65943f6aa3ba2f4a289b50bc024d18f')
    result_company = dadata.find_by_id("party", pk)
    error = ''
    try:
        result_company[0]['data']['inn'] == pk
    except ValueError:
        error = 'Произошла ошибка сохранения: форма содержала некоректные данные (ValueError)'
    except IndexError:
        error = 'Произошла ошибка сохранения: форма содержала некоректные данные (IndexError)'
    else:
        form = Organization(
            full_name=result_company[0]['data']['name']['full_with_opf'],
            short_name=result_company[0]['data']['name']['short_with_opf'],
            inn=result_company[0]['data']['inn'],
            kpp=result_company[0]['data']['kpp'],
            ur_adres=result_company[0]['data']['address']['unrestricted_value'],
            management_full_name=result_company[0]['data']['management']['name'].lower().title(),
            management_post=result_company[0]['data']['management']['post'].lower().capitalize()
        )
        form.save()
        # Получаем id только что созданной записи
        # new_organization_id = form.id
        return redirect('organization-detail', pk=form.id)
    context = {
        'error': error
    }
    return render(request, 'Accounting/about.html', context)


@login_required
def organization_create(request):
    error = ''
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('organization-detail', pk=obj.id)
        else:
            error = 'Форма была неверной'

    form = OrganizationForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'Accounting/organization-create.html', context)

@login_required
def dogovor_detail(request, pk):
    # Функция запускает детальную страницу Договра
    dogovor_list = Dogovor.objects.get(id=pk)
    service_list = Service.objects.filter(dogovor=dogovor_list)
    # Добавляем в список услгу расчет периода
    for el in service_list:
        el.period = (el.date_end - el.date_start).days + 1
    # Добавляем в список услгу расчет задолженности
    for el in service_list:
        el.debt = el.price - el.payment_made
    context = {
        'dogovor_list': dogovor_list,
        'service_list': service_list
    }
    return render(request, 'Accounting/dogovor-detail.html', context)

@login_required
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


@login_required
def dogovor_create(request):
    error = ''
    if request.method == 'POST':
        form = DogovorForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('dogovor-detail', pk=obj.id)
        else:
            error = 'Форма была неверной'
    form = DogovorForm(initial={'contract_completed': "true"})
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'Accounting/dogovor-create.html', context)


@login_required
def dogovor_create_target(request, pk):
    organization = Organization.objects.get(id=pk)
    error = ''
    if request.method == 'POST':
        form = DogovorForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('dogovor-detail', pk=obj.id)
        else:
            error = 'Форма была неверной'
    form = DogovorForm(initial={'organization': organization.id, 'contract_completed': "true", 'date_of_signing': datetime.datetime.now().strftime ("%d.%m.%Y")})
    context = {
        'form': form,
        'organization': organization,
        'error': error
    }
    return render(request, 'Accounting/dogovor-create.html', context)

@login_required
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

@login_required
def service_detail(request, pk):
    # Функция запускает детальную страницу Услуги
    service_list = Service.objects.get(id=pk)
    # Считаем сколько дней период между датами
    service_list.period = (service_list.date_end - service_list.date_start).days + 1
    # Считаем остаток задолжености
    service_list.debt = service_list.price - service_list.payment_made
    return render(request, 'Accounting/service-detail.html', {'service_list': service_list})

@login_required
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

@login_required
def service_create(request):
    error = ''
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('service-detail', pk=obj.id)
        else:
            error = 'Форма была неверной'

    form = ServiceForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'Accounting/service-create.html', context)

@login_required
def service_create_target(request, pk):
    dogovor = Dogovor.objects.get(id=pk)
    error = ''
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('service-detail', pk=obj.pk)
        else:
            error = 'Форма была неверной'

    form = ServiceForm(initial={'dogovor': dogovor.id, 'service_name': dogovor.service_type, 'price': dogovor.basic_price, 'payment_made': 0})
    context = {
        'form': form,
        'dogovor': dogovor,
        'error': error
    }
    return render(request, 'Accounting/service-create.html', context)

@login_required
def service_generate_bill(request, pk):
    service_list = Service.objects.get(id=pk)
    dogovor_list = Dogovor.objects.get(id=service_list.dogovor.id)
    generate_bill(dogovor_list, service_list)
    # Блок - Скачиваем файл в браузере
    # Генерируем имя конечного файла
    file_name = f'{service_list.dogovor.organization.short_name} bill N {service_list.id} {service_list.service_name}'
    file_name = translit(file_name)  # Переводим в транслит, тк с кириллицей проблемы.
    # Создайте объект HttpResponse, чтобы отправить файл в браузер
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f"attachment; filename={file_name}.docx"
    # Откройте созданный файл и запишите его содержимое в ответ
    with open("static/Generate/generated.docx", "rb") as f:
        response.write(f.read())
    return response

@login_required
def service_generate_act(request, pk):
    service_list = Service.objects.get(id=pk)
    dogovor_list = Dogovor.objects.get(id=service_list.dogovor.id)
    generate_act(dogovor_list, service_list)
    # Блок - Скачиваем файл в браузере
    # Генерируем имя конечного файла
    file_name = f'{service_list.dogovor.organization.short_name} Act N {service_list.id} {service_list.service_name}'
    file_name = translit(file_name)  # Переводим в транслит, тк с кириллицей проблемы.
    # Создайте объект HttpResponse, чтобы отправить файл в браузер
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f"attachment; filename={file_name}.docx"
    # Откройте созданный файл и запишите его содержимое в ответ
    with open("static/Generate/generated.docx", "rb") as f:
        response.write(f.read())
    return response
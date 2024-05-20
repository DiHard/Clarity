from docxtpl import DocxTemplate
import os
# Библиотека: pip install docxtpl
# pip install transliterate
import transliterate


# print(os.path.abspath('static/Generate/Bill_template (1).docx'))
def translit(ru_stroka):
# Транслитерация строки
    transliterated_string = transliterate.translit(ru_stroka, 'ru', reversed=True)
    return transliterated_string

def generate(dogovor_list):
    doc = DocxTemplate("static/Generate/Dogovor_template.docx")

    context = {
        'dogovor_list_nomer_dogovora': dogovor_list.nomer_dogovora,
        'dogovor_list_date_of_signing': dogovor_list.date_of_signing,
        'dogovor_list_organization_management_post': dogovor_list.organization.management_post,
        'dogovor_list_organization_management_full_name': dogovor_list.organization.management_full_name,
        'dogovor_list_site': dogovor_list.web_site,
        'dogovor_list_basic_price': dogovor_list.basic_price,
        'dogovor_list_organization_inn': dogovor_list.organization.inn,
        'dogovor_list_organization_kpp': dogovor_list.organization.kpp,
        'dogovor_list_organization_ur_adres': dogovor_list.organization.ur_adres,
        'dogovor_list_organization_full_name': dogovor_list.organization.full_name,
        'dogovor_list_organization_short_name': dogovor_list.organization.short_name
    }
    doc.render(context)
    doc.save("static/Generate/generated.docx")

def generate_bill(dogovor_list, service_list):
    doc = DocxTemplate("static/Generate/Bill_template.docx")
    context = {
        'dogovor_list_nomer_dogovora': dogovor_list.nomer_dogovora,
        'dogovor_list_date_of_signing': dogovor_list.date_of_signing,
        'dogovor_list_organization_management_post': dogovor_list.organization.management_post,
        'dogovor_list_organization_management_full_name': dogovor_list.organization.management_full_name,
        'dogovor_list_site': dogovor_list.web_site,
        'dogovor_list_basic_price': dogovor_list.basic_price,
        'dogovor_list_organization_inn': dogovor_list.organization.inn,
        'dogovor_list_organization_kpp': dogovor_list.organization.kpp,
        'dogovor_list_organization_ur_adres': dogovor_list.organization.ur_adres,
        'dogovor_list_organization_full_name': dogovor_list.organization.full_name,
        'dogovor_list_organization_short_name': dogovor_list.organization.short_name,
        'service_list_id': service_list.id
    }
    doc.render(context)
    doc.save("static/Generate/generated.docx")
def generate_act(dogovor_list, service_list):
    doc = DocxTemplate("static/Generate/Act_template.docx")
    context = {
        'dogovor_list_nomer_dogovora': dogovor_list.nomer_dogovora,
        'dogovor_list_date_of_signing': dogovor_list.date_of_signing,
        'dogovor_list_organization_management_post': dogovor_list.organization.management_post,
        'dogovor_list_organization_management_full_name': dogovor_list.organization.management_full_name,
        'dogovor_list_site': dogovor_list.web_site,
        'dogovor_list_basic_price': dogovor_list.basic_price,
        'dogovor_list_organization_inn': dogovor_list.organization.inn,
        'dogovor_list_organization_kpp': dogovor_list.organization.kpp,
        'dogovor_list_organization_ur_adres': dogovor_list.organization.ur_adres,
        'dogovor_list_organization_full_name': dogovor_list.organization.full_name,
        'dogovor_list_organization_short_name': dogovor_list.organization.short_name,
        'service_list_id': service_list.id
    }
    doc.render(context)
    doc.save("static/Generate/generated.docx")
from docxtpl import DocxTemplate
# Библиотека: pip install docxtpl
# pip install transliterate

import transliterate

def translit(ru_stroka):
# Транслитерация строки
    transliterated_string = transliterate.translit(ru_stroka, 'ru', reversed=True)
    return transliterated_string

def generate(dogovor_list):
    doc = DocxTemplate("static/Generate/dogovor_template.docx")
    context = {'COMPANY_NAME': dogovor_list.organization.full_name, 'DIRECTOR_NAME': 'Добрынин Иван Федорович'}
    doc.render(context)
    doc.save("static/Generate/generated.docx")


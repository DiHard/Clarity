from dadata import Dadata


dadata = Dadata('0fc7d60da65943f6aa3ba2f4a289b50bc024d18f')


inn = '7707083893'


def add_bu_inn(inn):
    result = dadata.find_by_id("party", inn)
    try:
        result[0]['data']['inn'] == inn
    except ValueError:
        print("Ошибка: не удалось найти организацию с указанным id")
    except IndexError:
        print("Ошибка: не удалось найти организацию с указанным id")
    else:
        print(result[0]['data']['inn'])
        print(result[0]['data']['name']['full_with_opf'])
        print(result[0]['data']['name']['short_with_opf'])
        print(result[0]['data']['management']['post'].lower().capitalize())
        print(result[0]['data']['management']['name'].lower().title())
        print(result[0]['data']['address']['unrestricted_value'])
        print(result[0]['data']['ogrn'])
        print(result[0]['data']['kpp'])

add_bu_inn(inn)
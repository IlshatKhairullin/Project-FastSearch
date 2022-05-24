import re
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.parser_perekrestok import Perekrestok_shop
from Parsers.Metro_Parser import Metro


def combine_parsers(product_name, address='Кубанская 54'):  # подумать про многопоточность, точно нужна при обработке запросов и скорее всего при парсинге 3-х сайтов
    user_products = 'Яндекс Лавка\n\n'

    lavka_dict = Yandex_Lavka_food_data(address)
    # perekrestok_dict = Perekrestok_shop(address)
    # metro_dict = Metro(address)

    for i in lavka_dict.keys():
        if product_name in i:
            if re.match(product_name+str(' '), i):
                user_products += f'{i}, цена - {str(lavka_dict[i][0])} рублей, вес - {lavka_dict[i][1]}\n'
    # дальше будет еще 2 цикла для перекрестка и метро
    return user_products

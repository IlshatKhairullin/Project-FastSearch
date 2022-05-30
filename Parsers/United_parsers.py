import psycopg2
from Database.config import host, user, password, db_name, port
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.parser_perekrestok import Perekrestok_shop
from Parsers.Metro_Parser import Metro


def combine_parsers(product_name, address='Кубанская 54'):  # у нас будет несколько баз данных и здесь при помощи
    # библиотеки для работы с координатами. какой склад ближе по заданному адресу, по тому и работаем

    user_products_lavka = 'Яндекс Лавка\n\n'
    user_products_metro = 'Метро\n\n'
    user_products_perekrestok = 'Перекресток\n\n'

    try:
        # подключение к базе данных
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )

        with connection.cursor() as cursor:
            sql = "SELECT product_name, price, amount FROM Lavka_food_data WHERE product_name ~* %s"
            search_product = "\m{}\M".format(product_name)
            cursor.execute(sql, (search_product,))
            prod_from_db = cursor.fetchall()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

    for i in prod_from_db:
        user_products_lavka += f'{i[0]}, цена - {str(i[1])} рублей, вес - {i[2]}\n'
    return user_products_lavka


if __name__ == '__main__':
    print(combine_parsers('^чипсы'))

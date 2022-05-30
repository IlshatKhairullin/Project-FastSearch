import geopy.distance
from geopy.geocoders import Nominatim
import psycopg2
from Database.config import host, user, password, db_name, port
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.parser_perekrestok import Perekrestok_shop
from Parsers.Metro_Parser import Metro


def combine_parsers(product_name, address):
    product_name = '^' + product_name
    
    locations_dict = {"Lavka_food_data_Aviastr": (55.85748, 49.08809),
                      "Lavka_food_data_Kirovski": (55.85707, 48.90532),
                      'Lavka_food_data_NovoSavin': (55.83703, 49.13472),
                      'Lavka_food_data_Moscovski': (55.8246, 49.05199),
                      'Lavka_food_data_Vahitovski': (55.78776, 49.1573),
                      'Lavka_food_data_Privoljski': (55.72513, 49.17319),
                      'Lavka_food_data_Sovetski': (55.78923, 49.22273),
                      }
    min_dist = 5000

    user_products_lavka = 'Яндекс Лавка\n\n'
    user_products_metro = 'Метро\n\n'
    user_products_perekrestok = 'Перекресток\n\n'

    geolocator = Nominatim(user_agent="email@email.com")
    location = geolocator.geocode(address + " Казань")

    pt1 = geopy.Point(location.latitude, location.longitude)

    for i in locations_dict.keys():
        pt2 = geopy.Point(locations_dict[i][0], locations_dict[i][1])
        dist = geopy.distance.distance(pt1, pt2).km
        if dist < min_dist:
            min_dist = dist
            data_base = i

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
            sql = "SELECT product_name, price, amount FROM {} WHERE product_name ~* %s".format(data_base)
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
    print(combine_parsers('чипсы', 'Кубанская 54'))

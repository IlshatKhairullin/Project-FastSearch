import geopy.distance
from geopy.geocoders import Nominatim
import psycopg2
from Database.config import host, user, password, db_name, port
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.parser_perekrestok import Perekrestok_shop
from Parsers.Metro_Parser import Metro


def combine_parsers(product_name, address):
    product_name = '^' + product_name

    lavka_locations_dict = {
        "Lavka_food_data_Aviastr": (55.85748, 49.08809),
        "Lavka_food_data_Kirovski": (55.85707, 48.90532),
        "Lavka_food_data_NovoSavin": (55.83703, 49.13472),
        "Lavka_food_data_Moscovski": (55.8246, 49.05199),
        "Lavka_food_data_Vahitovski": (55.78776, 49.1573),
        "Lavka_food_data_Privoljski": (55.72513, 49.17319),
        "Lavka_food_data_Sovetski": (55.78923, 49.22273),
                            }
    metro_locations_dict = {"Metro_food_data_Center": (55.73226, 49.13105),
                            "Metro_food_data_Rest_of_Kazan": (55.81227, 49.08195)
                            }
    perekrestok_locations_dict = {"Perekrestok_food_data_Aviastr": (55.82122, 49.09256),
                            "Perekrestok_food_data_Kirovski": (55.81814, 48.90073),
                            "Perekrestok_food_data_NovoSavin": (55.82743, 49.1547),
                            "Perekrestok_food_data_Moscovski": (55.83032, 49.06203),
                            "Perekrestok_food_data_Vahitovski": (55.77857, 49.12957),
                            "Perekrestok_food_data_Privoljski": (55.7485, 49.20703),
                            "Perekrestok_food_data_Sovetski": (55.81589, 49.18211)
                                  }
    min_dist = 5000

    user_products_lavka = "Яндекс Лавка\n\n"
    user_products_metro = "Метро\n\n"
    user_products_perekrestok = "Перекресток\n\n"

    geolocator = Nominatim(user_agent="email@email.com")
    location = geolocator.geocode(address + " Казань")

    pt1 = geopy.Point(location.latitude, location.longitude)

    for i in lavka_locations_dict.keys():
        pt2 = geopy.Point(lavka_locations_dict[i][0], lavka_locations_dict[i][1])
        dist = geopy.distance.distance(pt1, pt2).km
        if dist < min_dist:
            min_dist = dist
            lavka_data_base = i

    for i in metro_locations_dict.keys():
        pt2 = geopy.Point(metro_locations_dict[i][0], metro_locations_dict[i][1])
        dist = geopy.distance.distance(pt1, pt2).km
        if dist < min_dist:
            min_dist = dist
            metro_data_base = i

    for i in perekrestok_locations_dict.keys():
        pt2 = geopy.Point(perekrestok_locations_dict[i][0], perekrestok_locations_dict[i][1])
        dist = geopy.distance.distance(pt1, pt2).km
        if dist < min_dist:
            min_dist = dist
            perekrestok_data_base = i

    if perekrestok_data_base == "Perekrestok_food_data_Kirovski":
        user_products_perekrestok += "Перекресток не доставляет на Ваш адрес"


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
            sql = "SELECT product_name, price, amount FROM {} WHERE product_name ~* %s".format(lavka_data_base)
            search_product = "\m{}\M".format(product_name)
            cursor.execute(sql, (search_product,))
            lavka_prod_from_db = cursor.fetchall()

        with connection.cursor() as cursor:
            sql = "SELECT product_name, price, amount FROM {} WHERE product_name ~* %s".format(metro_data_base)
            search_product = "\m{}\M".format(product_name)
            cursor.execute(sql, (search_product,))
            metro_prod_from_db = cursor.fetchall()

        with connection.cursor() as cursor:
            sql = "SELECT product_name, price, amount FROM {} WHERE product_name ~* %s".format(perekrestok_data_base)
            search_product = "\m{}\M".format(product_name)
            cursor.execute(sql, (search_product,))
            perekrestok_prod_from_db = cursor.fetchall()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

    for product_data_L in lavka_prod_from_db:
        user_products_lavka += f"{product_data_L[0]}, цена - {str(product_data_L[1])} рублей, вес - {product_data_L[2]}\n"

    for product_data_M in metro_prod_from_db:
        user_products_metro += f"{product_data_M[0]}, цена - {str(product_data_M[1])} рублей, вес - {product_data_M[2]}\n"

    if perekrestok_data_base != "Perekrestok_food_data_Kirovski":
        for product_data_P in perekrestok_prod_from_db:
            user_products_perekrestok += f"{product_data_P[0]}, цена - {str(product_data_P[1])} рублей, вес - " \
                                         f"{product_data_P[2]}\n"

    return user_products_lavka, user_products_metro, user_products_perekrestok


if __name__ == '__main__':
    print(combine_parsers('кефир', 'Кубанская 54'))

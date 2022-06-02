import psycopg2
from time import sleep
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.Metro_Parser import Metro
from Parsers.parser_perekrestok import Perekrestok_shop
from Database.config import host, user, password, db_name, port


def refresh_data_base():
    lavka_district_dict = {
        "Авиастроительный район": ("Aviastr", "улица Лукина, 3А"),
        "Кировский район": ("Kirovski", "просп. Ильгама Шакирова, 9"),
        "Ново-Савиновский район": ("NovoSavin", "ул. Фатыха Амирхана, 19А"),
        "Московский район": ("Moscovski", "улица Кулахметова, 9"),
        "Вахитовский район": ("Vahitovski", "улица Достоевского, 79"),
        "Приволжский район": ("Privoljski", "ул. Рауиса Гареева, 110"),
        "Советский район": ("Sovetski", "ул. Академика Глушко, 30А")
    }

    metro_district_dict = {
        "Центр Казани": ("Center", "Тихорецая улица 4"),
        "Остальная Казань": ("Rest_of_Kazan", "улица Мулпланура Вахитова 4")
    }

    # в Кировский район перекресток не доставляет
    perekrestok_district_dict = {
        "Авиастроительный район": ("Aviastr", "Ибрагимова пр-кт 56"),
        "Ново-Савиновский район": ("NovoSavin", "пр-т. Хусаина Ямашева, 93"),
        "Московский район": ("Moscovski", "Кулахметова ул 28"),
        "Вахитовский район": ("Vahitovski", "Спартаковская д 6"),
        "Приволжский район": ("Privoljski", "Победа пр-т 50Б"),
        "Советский район": ("Sovetski", "Сибирский Тракт д 34")
    }

    while True:
        sleep(3600)

        try:
            # подключение к базе данных
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port
            )
            connection.autocommit = True  # чтобы автоматически сохранялись изменения, после запроса в sql

            # нужно создать объект курсор, для выполнения sql команд
            with connection.cursor() as cursor:  # если написать так, то не придется потом закрывать
                cursor.execute(
                    "SELECT version();"
                )

            for district_L in lavka_district_dict.values():
                lavka_data_dict = Yandex_Lavka_food_data(district_L[1])

                try:
                    # создание изначальной таблицы
                    with connection.cursor() as cursor:
                        sql = "CREATE TABLE {}(product_name varchar(200) NOT NULL, price smallint NOT NULL, " \
                              "amount varchar(100) NOT NULL)".format("Lavka_food_data_" + district_L[0])
                        cursor.execute(sql)
                        print("[INFO] Table Lavka created successfully")
                except:
                    continue

                finally:
                    # обновление данных в таблицах
                    with connection.cursor() as cursor:
                        for prod_data1 in lavka_data_dict.keys():
                            sql_test = "SELECT product_name FROM {} WHERE product_name = %s".format(
                                "Lavka_food_data_" + district_L[0])
                            cursor.execute(sql_test, (prod_data1,))
                            a = cursor.fetchone()

                            if a is None:
                                cursor.execute(
                                    "INSERT INTO {} (product_name, price, amount) VALUES (%s, %s, %s)".format(
                                        "Lavka_food_data_" + district_L[0]),
                                    (prod_data1, lavka_data_dict[prod_data1][0], lavka_data_dict[prod_data1][1])
                                )
                            else:
                                sql = "UPDATE {} SET (product_name, price, amount) = (%s, %s, %s) WHERE product_name " \
                                      "= %s".format("Lavka_food_data_" + district_L[0])
                                cursor.execute(sql, (prod_data1, lavka_data_dict[prod_data1][0],
                                                     lavka_data_dict[prod_data1][1], prod_data1))

                    print(f"[INFO] Data {'Lavka_food_data_' + district_L[0]} was successfully updated")

            for district_M in metro_district_dict.values():
                metro_data_dict = Metro(district_M[1])

                try:
                    # создание изначальной таблицы
                    with connection.cursor() as cursor:
                        sql = "CREATE TABLE {}(product_name varchar(200) NOT NULL, price smallint NOT NULL, " \
                              "amount varchar(100) NOT NULL)".format("Metro_food_data_" + district_M[0])
                        cursor.execute(sql)
                        print("[INFO] Table Metro created successfully")
                except:
                    continue

                finally:
                    with connection.cursor() as cursor:
                        for prod_data2 in metro_data_dict.keys():

                            sql_test = "SELECT product_name FROM {} WHERE product_name = %s".format(
                                "Metro_food_data_" + district_M[0])
                            cursor.execute(sql_test, (prod_data2,))
                            a = cursor.fetchone()

                            if a is None:
                                cursor.execute(
                                    "INSERT INTO {} (product_name, price, amount) VALUES (%s, %s, %s)".format(
                                        "Metro_food_data_" + district_M[0]),
                                    (prod_data2, metro_data_dict[prod_data2][0], metro_data_dict[prod_data2][1])
                                )
                            else:
                                sql = "UPDATE {} SET (product_name, price, amount) = (%s, %s, %s) " \
                                      "WHERE product_name = %s".format("Metro_food_data_" + district_M[0])
                                cursor.execute(sql, (prod_data2, metro_data_dict[prod_data2][0],
                                                     metro_data_dict[prod_data2][1], prod_data2))

                    print(f"[INFO] Data {'Metro_food_data_' + district_M[0]} was successfully updated")

            for district_P in perekrestok_district_dict.values():
                perekrestok_data_dict = Perekrestok_shop(district_P[1])

                try:
                    # создание изначальной таблицы
                    with connection.cursor() as cursor:
                        sql = "CREATE TABLE {}(product_name varchar(200) NOT NULL, price smallint NOT NULL, " \
                              "amount varchar(100) NOT NULL)".format("Perekrestok_food_data_" + district_P[0])
                        cursor.execute(sql)
                        print("[INFO] Table Perekrestok created successfully")
                except:
                    continue

                finally:

                    with connection.cursor() as cursor:
                        for prod_data3 in perekrestok_data_dict.keys():

                            sql_test = "SELECT product_name FROM {} " \
                                       "WHERE product_name = %s".format("Perekrestok_food_data_" + district_P[0])
                            cursor.execute(sql_test, (prod_data3,))
                            a = cursor.fetchone()

                            if a is None:
                                cursor.execute(
                                    "INSERT INTO {} (product_name, price, amount) "
                                    "VALUES (%s, %s, %s)".format("Perekrestok_food_data_" + district_P[0]),
                                    (prod_data3, perekrestok_data_dict[prod_data3][0],
                                     perekrestok_data_dict[prod_data3][1])
                                )
                            else:
                                sql = "UPDATE {} SET (product_name, price, amount) = (%s, %s, %s) " \
                                      "WHERE product_name = %s".format("Perekrestok_food_data_" + district_P[0])
                                cursor.execute(sql, (prod_data3, perekrestok_data_dict[prod_data3][0],
                                                     perekrestok_data_dict[prod_data3][1], prod_data3))

                    print(f"[INFO] Data {'Perekrestok_food_data_' + district_P[0]} was successfully updated")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")


if __name__ == '__main__':
    refresh_data_base()

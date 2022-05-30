import psycopg2
from time import sleep
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.Metro_Parser import Metro
from Parsers.parser_perekrestok import Perekrestok_shop
from Database.config import host, user, password, db_name, port


def refresh_data_base():
    district_dict = {"Кировский район": ("Kirovski", "просп. Ильгама Шакирова, 9"),
                     "Авиастроительный район": ("Aviastr", "улица Лукина, 3А"),
                     "Ново-Савиновский район": ("NovoSavin", "ул. Фатыха Амирхана, 19А"),
                     "Московский район": ("Moscovski", "улица Кулахметова, 9"),
                     "Вахитовский район": ("Vahitovski", "улица Достоевского, 79"),
                     "Приволжский район": ("Privoljski", "ул. Рауиса Гареева, 110"),
                     "Советский район": ("Sovetski", "ул. Академика Глушко, 30А")}

    while True:
        sleep(3600)
        for i in district_dict.values():
            lavka_data_dict = Yandex_Lavka_food_data(i[1])
            # metro_data_dict = Metro('')  # дописать sql-запросы для остальных 2-ух парсеров + разделить по складам
            # perekrestok_data_dict = Perekrestok_shop('')

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

                try:
                    # создание изначальной таблицы
                    with connection.cursor() as cursor:
                        sql = "CREATE TABLE {}(product_name varchar(200) NOT NULL, price smallint NOT NULL, " \
                              "amount varchar(100) NOT NULL)".format("Lavka_food_data_" + i[0])
                        cursor.execute(sql)

                        print("[INFO] Table created successfully")

                except:
                    continue

                finally:

                    # обновление данных в таблицах
                    with connection.cursor() as cursor:
                        for i1 in lavka_data_dict.keys():

                            sql_test = "SELECT product_name FROM {} WHERE product_name = %s".format(
                                "Lavka_food_data_" + i[0])
                            cursor.execute(sql_test, (i1,))
                            a = cursor.fetchone()

                            if a is None:
                                cursor.execute(
                                    "INSERT INTO {} (product_name, price, amount) VALUES (%s, %s, %s)".format(
                                        "Lavka_food_data_" + i[0]),
                                    (i1, lavka_data_dict[i1][0], lavka_data_dict[i1][1])
                                )
                            else:
                                sql = "UPDATE {} SET (product_name, price, amount) = (%s, %s, %s)".format(
                                    "Lavka_food_data_" + i[0])
                                cursor.execute(sql, (i1, lavka_data_dict[i1][0], lavka_data_dict[i1][1]))

                    print(f"[INFO] Data {'Lavka_food_data_' + i[0]} was successfully updated")

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)

            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")


if __name__ == '__main__':
    refresh_data_base()

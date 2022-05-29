import psycopg2
from time import sleep
from Parsers.Yandex_lavka_parser import Yandex_Lavka_food_data
from Parsers.Metro_Parser import Metro
from Parsers.parser_perekrestok import Perekrestok_shop
from Database.config import host, user, password, db_name, port


def refresh_data_base():

    while True:
        sleep(10)
        lavka_data_dict = Yandex_Lavka_food_data('')
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

            # создание изначальной таблицы
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """CREATE TABLE Yandex_Lavka_food_data(
                        product_name varchar(200) NOT NULL,
                        price smallint NOT NULL,
                        amount varchar(100) NOT NULL);"""
                    )

                    print("[INFO] Table created successfully")
            except:
                continue

            # удаление старой таблицы
            with connection.cursor() as cursor:
                cursor.execute(
                    """DROP TABLE Yandex_Lavka_food_data;"""
                )

                print("[INFO] Table Yandex_Lavka_food_data was deleted")

            # создание новой таблицы
            with connection.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE Yandex_Lavka_food_data(
                    product_name varchar(200) NOT NULL,
                    price smallint NOT NULL,
                    amount varchar(100) NOT NULL);"""
                )

                print("[INFO] Table created successfully")

            # добавление данных в таблицу
            with connection.cursor() as cursor:
                for i in lavka_data_dict.keys():
                    cursor.execute(
                        "INSERT INTO Yandex_Lavka_food_data (product_name, price, amount) VALUES (%s, %s, %s)",
                        (i, lavka_data_dict[i][0], lavka_data_dict[i][1])
                        )

            print("[INFO] Data was successfully inserted")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")


if __name__ == '__main__':
    refresh_data_base()

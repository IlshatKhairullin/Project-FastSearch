import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from time import sleep
import lxml


def Metro(address):
    these_keys = address.split()

    # Сам сайт
    URL = 'https://online.metro-cc.ru'

    # Мой headers
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.50"
    }
    # Эмилуятор гугл хрома
    options = webdriver.ChromeOptions()
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.72")
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Сам драйвер гугла
    driver = webdriver.Chrome(
        executable_path=r'C:\Python_Project_Kfu\Ozon\Main\chromedriver.exe',
        options=options
    )

    # Блок ввод Адреса доставки(и закрытия рекламы)
    try:
        driver.get(url=URL)
        sleep(5)
        try:
            # Нажали на адрес доставки
            driver.find_element_by_class_name('header-delivery-info__details-button').click()
            sleep(2)

            # Ввод в поле (адреса доставки)
            address_string = driver.find_element_by_id(
                "search-input")
            sleep(2)

            # Вставляем ключ
            address_string.send_keys(Keys.LEFT_CONTROL + 'a')
            address_string.send_keys(Keys.BACKSPACE)
            sleep(3)

            # Ввод адреса  Казань, Кубанская улица, 62/14
            address_string.send_keys(
                'Россия, Республика Татарстан, Казань, ' + these_keys[0] + ' улица, ' + these_keys[1])
            sleep(3)

            # Делаем спейс и ждём (выбор адреса предложенной строкой)
            address_string.send_keys(Keys.SPACE)
            sleep(5)

            # Нажимаем сохранить адрес
            driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div[1]/div[3]/div[1]/button').click()
            sleep(3)

            # Нажимаем сохранить адрес (2,так как 1 не всегда срабатывает)
            driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div[1]/div[3]/div[1]/button').click()
            sleep(3)

            # Наш город - Казань? (Да)
            driver.find_element_by_xpath(
                '/html/body/div[3]/div/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/button[1]').click()
            sleep(3)

            # Открываем категории
            driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/button').click()
            sleep(3)

        except Exception as ex:
            print(ex)

        with open('html_code.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)

    with open('html_code.html', 'r', encoding='utf-8') as file:  # нужна только для написания кода
        src = file.read()

    # Объект супа
    soup = BeautifulSoup(src, "lxml")

    # ссылки на все категории
    links = soup.find_all('a', class_='side-menu_list--link')

    all_categories_dict = {}

    # Цикл категория: ссылка
    for item in links:
        item_text = item.text
        item_href = 'https://online.metro-cc.ru' + item.get('href')
        # print(f'{item_text}: {item_href}')

        all_categories_dict[item_text] = item_href

    # Файл json со всеми категориями
    with open('all_categories.json', 'w') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

    # Считываем
    with open('all_categories.json') as file:
        all_categories = json.load(file)

    product_prices = []
    product_names = []
    product_amount = []

    # Достали все ссылки категорий
    for i in list(all_categories.values())[1:11 + 1]:
        driver.get(i)
        driver.implicitly_wait(5)

        # записали код html категории
        with open('html_code.html', 'w', encoding='utf-8') as file:  # записали кодировку отдельной категории
            file.write(driver.page_source)  # кодировки категорий постоянно будут перезаписываться

        # считали код html категории
        with open('html_code.html', 'r', encoding='utf-8') as file2:
            full_page = file2.read()

        # Объект супа
        soup = BeautifulSoup(full_page, 'lxml')

        a_lot_of_product_data = soup.find_all('div', class_='catalog-item__top')

        for product_data in a_lot_of_product_data:

            product_price = product_data.find('div', class_='catalog-item_price-lvl_current')
            try:
                product_prices.append(int(str(product_price.text).strip()[:str(product_price.text).strip().index(' ')]))
            except:
                continue

            product_name = product_data.find('a', class_='catalog-item_name')
            try:
                product_names.append(product_name.text.strip())
            except:
                continue

            product_amounts = product_data.find()
    driver.close()
    driver.quit()

    json_dict = {product_names[i]: [product_prices[i]] for i in range(len(product_names))}

    with open("Metro_json", "w") as file:
        json.dump(json_dict, file, indent=4, ensure_ascii=False)

    with open('Metro_json', 'r') as file:
        data = json.load(file)
        print(data)


def main():
    Metro('Кубанская 62/14')


if __name__ == "__main__":
    main()

from selenium import webdriver
from bs4 import BeautifulSoup
import json
from time import sleep
from selenium.webdriver.common.keys import Keys

def Perekrestok_shop(address):  # адрес доставки. название улицы_пробел_номер дома, только улица и номер дома
    these_keys = address.split()
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; U; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/101.0.4853.211 Chrome/101.0.4853.211 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\пк\PycharmProjects\pythonProject45\chromedriver.exe',
        options=options
    )
    url = 'https://www.perekrestok.ru/cat'

    try:
        driver.get(url=url)
        driver.implicitly_wait(6)

        driver.find_element_by_xpath('/html/body/div[1]/div/header/div[1]/div[1]/div[2]/div/button').click()
        sleep(2)

        address_string = driver.find_element_by_class_name('react-select__input').find_element_by_id(
            'react-select-2-input')
        sleep(2)

        address_string.send_keys(Keys.LEFT_CONTROL + 'a') # удаляем если вдруг что-то лишнее в адресной строке имеется
        address_string.send_keys(Keys.BACKSPACE) # удаляем если вдруг что-то лишнее в адресной строке имеется
        sleep(3)

        address_string.send_keys('г Казань, ул ' + these_keys[0] + ' ' + these_keys[1] + ' ,д ' + these_keys[2])
        sleep(2)

        address_string.send_keys(Keys.ENTER)
        if driver.find_element_by_xpath(
                '/html/body/div[8]/div/div/div/div/div/div[1]/div/div/div[1]').text != 'Мы доставляем к вам!':
            return "По этому аресу доставки нет"
        address_string.send_keys(Keys.ENTER)
        sleep(1)



        with open('html_сode.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source) #записываем html код страницы.

    except Exception as ex:
        print(ex)

    with open('html_сode.html', 'r', encoding='utf-8') as file1:  # данная строка нужна только для написания кода в bs4.
        src = file1.read()

    soup = BeautifulSoup(src, 'lxml') #парсим код с помощью парсера lxml.

    all_products = soup.findAll(class_="sc-dlfnbm jwhrZg catalog__column") #все категории. записываем как список.

    all_categories_dict = {} #создаём словарь, в нём будем хранить категорию - ссылку.

    for item in all_products:
        item_text = item.text.strip()  # strip() чтоб всяких /n /n /n в json файле не выводилось
        item_href = "https://www.perekrestok.ru" + item.find(class_='sc-bkzZxe fAwjHM').get('href')

        all_categories_dict[item_text] = item_href  #заполняем наш словарь, ключом будет категория, значением.

    with open("all_categories_dict.json", "w", encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False) #сохраняем наш словарь в json файл.

    with open("all_categories_dict.json", encoding='utf-8') as file:
        all_categories = json.load(file)

    print(all_categories)

    name_list = []
    price_list = []
    weight_list = []

    for category_name, category_href in all_categories.items(): #заменяем символы из 'rep' на '_' , ДЛЯ КРАСОТЫ(необязательно).
        rep = [',', ' ', '-']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")

        driver.get(url=category_href)
        driver.implicitly_wait(5)

        with open("link_for_each_category.html", 'w', encoding='utf-8') as file3:
            file3.write(driver.page_source)  # сохраняем html файл каждой категории

        with open("link_for_each_category.html", encoding='utf-8') as file4:
            src = file4.read()

        soup = BeautifulSoup(src, "lxml")  # создаём объект класса BeautifulSoup.

        block = soup.findAll(class_='swiper-slide swiper-slide-visible swiper-slide-active')
        for item in block:
            title = item.find(class_="product-card__title").text.strip()  # наименование товара.
            price_list.append(item.find(class_='price-new').text.strip()[:-5])  # цена товара(добавляем в список).

            weight_list.append(title[title.rindex(' ') + 1:])  #вес товара(добавляем в список).
            name_list.append(title[:title.rindex(' ') - 1]) #name товара(добавляем в список).

    driver.close()
    driver.quit()

    json_dict = {name_list[i]: [price_list[i], weight_list[i]] for i in range(len(name_list))}

    with open('perekrestok.json', 'w', encoding='utf-8') as file5:
        json.dump(json_dict, file5, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    Perekrestok_shop('Академика Парина 4141141')
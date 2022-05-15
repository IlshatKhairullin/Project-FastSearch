from selenium import webdriver
from bs4 import BeautifulSoup
import json
from time import sleep
from selenium.webdriver.common.keys import Keys

def Perekrestok_shop(address):  # адрес доставки. название улицы_пробел_номер дома, только улица и номер дома
    these_keys = address.split()
    options = webdriver.ChromeOptions()
    options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4846.194 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(
            executable_path=r'C:\Users\пк\PycharmProjects\pythonProject38\chromedriver.exe',
            options=options
    )
    url = 'https://www.perekrestok.ru/cat'

    try:
        driver.get(url=url)
        driver.implicitly_wait(5)

        driver.find_element_by_xpath('/html/body/div[1]/div/header/div[1]/div[1]/div[2]/div/button').click()
        sleep(5)

        address_string = driver.find_element_by_class_name('react-select__input').find_element_by_id(
            'react-select-2-input')
        sleep(3)

        address_string.send_keys('г Казань, ул ' + these_keys[0] + ' ' + these_keys[1] + ' ,д ' + these_keys[2])
        sleep(2)
        address_string.send_keys(Keys.ENTER)
        address_string.send_keys(Keys.ENTER)

        sleep(4)

        with open('html_сode.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)

    with open('html_сode.html', 'r', encoding='utf-8') as file:  # данная строка нужна только для написания кода
        src = file.read()

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src) #на всякий случай. вдруг сайт тебя забанит.

    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_products = soup.findAll(class_="sc-dlfnbm jwhrZg")

    all_categories_dict = {}

    for item in all_products:
        item_text = item.text.strip() #strip() чтоб всяких /n /n /n в json файле не выводилось
        item_href = "https://www.perekrestok.ru" + item.find(class_='sc-bkzZxe fAwjHM').get('href')

        all_categories_dict[item_text] = item_href #наполняем наш словарь ключом будет категория, значением - ссылка(нужен джейсон)
    
    with open("all_categories_dict.json", "w", encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False) #сохраняем в json файл для удобства. ensure - чтоб русские символы читались
    with open("all_categories_dict.json", encoding='utf-8') as file:
        all_categories = json.load(file)

    name_list=[]
    price_list=[]
    weight_list=[]

    for category_name, category_href in all_categories.items():

        rep =[',', ' ', '-']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")


        driver.get(url=category_href)
        driver.implicitly_wait(5)

        with open("tapkin.html", 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

        with open("tapkin.html", encoding='utf-8') as file2:
            src = file2.read()

        soup = BeautifulSoup(src, "lxml")

        block = soup.findAll(class_='swiper-slide swiper-slide-visible swiper-slide-active')



        for item in block:
            title = item.find(class_="product-card__title").text.strip()
            price_list.append(item.find(class_='price-new').text.strip()[:-5])

            weight_list.append(title[title.rindex(' ')+1:])
            name_list.append(title[:title.rindex(' ')-1])



    driver.close()
    driver.quit()
    print(f'Список имен: {name_list}')
    print(f'Спсиок веса: {weight_list}')
    print(f'Список цен: {price_list}')
    json_dict = {name_list[i]: [price_list[i], weight_list[i]] for i in range(len(name_list))}

    with open('perekrestok.json', 'w') as file:
        json.dump(json_dict, file)


if __name__ == '__main__':
    Perekrestok_shop('Академика Парина 4')

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


def Yandex_Lavka_food_data(address):  # адрес доставки. название улицы_пробел_номер дома, только улица и номер дома

    """блок кода для получения полной кодировки сайта"""
    url = 'https://lavka.yandex.ru/43/'

    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')

    options.add_argument('--headless')  # ДЛЯ тестировщика - закоментить эту строку, для удобства

    driver = webdriver.Chrome(
        executable_path=r'C:\Users\Ильшат\FastSearch_Project\Parsers\chromedriver.exe',
        options=options
    )

    try:
        driver.get(url=url)
        driver.implicitly_wait(5)

        driver.find_element_by_xpath("/html/body/div/header/div[4]/button").click()  # четвертый div. copy full xpath
        driver.implicitly_wait(5)  # как только прогрузился сайт, сразу начинается next действие
        address_string = driver.find_element_by_class_name('i164506l')
        sleep(2)
        address_string.send_keys(Keys.LEFT_CONTROL + 'a')
        sleep(1)
        address_string.send_keys('Россия, Республика Татарстан, Казань, ' + str(address))
        sleep(2)
        address_string.send_keys(Keys.SPACE)
        sleep(2)
        driver.find_element_by_class_name('l1xltboq').click()
        sleep(2)

        if driver.find_element_by_css_selector('body > div:nth-child(11) > div:nth-child(3) > div > div > div > div.mdq9h8o > div > div.a1hnj29o > div > div.c1d3b3d4 > div > div.t1vrfrqt.t18stym3.bw441np.r88klks.r1dbrdpx.n10d4det.l14lhr1r').text != 'Ура, Лавка доставляет к вам':
            return "По данному адресу Яндекс Лавка не доставляет"

        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button').click()
        sleep(2)

        with open('html_code.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)

    with open('html_code.html', 'r', encoding='utf-8') as file:  # данная строка нужна только для написания кода
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')  # lxml - самый быстрый парсер, качать придется через pip install lxml

    categories = soup.find_all('ul', class_='c1juywv9')  # запарсили все категории, чтобы не прописывать по отдельности

    """блок кода для получения url всех категорий"""
    category_urls = []
    half_category_urls = []
    for half_category in categories:
        half_category_url = half_category.find_all('a', class_='azs7ia1')
        for i in half_category_url:
            half_category_urls.append(i)

    for category in half_category_urls:
        category_url = 'https://lavka.yandex.ru' + category.get('href')
        category_urls.append(category_url)

    product_prices = []
    product_names = []
    product_amounts = []

    for category_url in category_urls[:-15]:  # последовательно пробегаем каждую категорию по url
        # до -15, тк парсим только продукты, далее -> аптечка, гигиена и тд

        driver.get(url=category_url)
        driver.implicitly_wait(5)

        with open('html_code.html', 'w', encoding='utf-8') as file:  # записали кодировку отдельной категории
            file.write(driver.page_source)  # кодировки категорий постоянно будут перезаписываться

        with open('html_code.html', 'r', encoding='utf-8') as file2:
            full_page = file2.read()

        soup = BeautifulSoup(full_page, 'lxml')

        a_lot_of_product_data = soup.find_all('div', class_='b13krz51')

        for product_data in a_lot_of_product_data:  # избегание лишней информации, иначе будут парсится нули для списка цен

            product_price = product_data.find('span', class_='t18stym3 b1clo64h m493tk9 m1fg51qz tnicrlv l14lhr1r')
            try:  # try - тк в процессе извлечения цены, имени... будут встречатся None, пока не найдем нужный класс
                product_prices.append(int(str(product_price.text).replace('\xa0₽', '')))
            except:
                continue

            product_name = product_data.find('h3',
                                             class_='toyntmz t18stym3 bw441np r88klks r1dbrdpx n10d4det l14lhr1r c10zw1sq')
            try:
                product_names.append(product_name.text)
            except:
                continue

            product_amount = product_data.find('span', class_='t18stym3 bw441np r88klks r1dbrdpx t1dh4tmf l14lhr1r')
            try:
                product_amounts.append(product_amount.text)
            except:
                continue

    driver.close()
    driver.quit()

    # пихаем всю инфу в словарь, название: [цена, вес/кол-во в одной упаковке]
    json_dict = {product_names[i]: [product_prices[i], product_amounts[i]] for i in range(len(product_names))}

    return json_dict

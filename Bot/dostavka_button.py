from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def Dostavka(address):  # адрес доставки. название улицы_пробел_номер дома, только улица и номер дома
    these_keys = address.split()
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4876.188 Safari/537.36")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\пк\PycharmProjects\pythonProject47\chromedriver.exe',
        options=options
    )
    url = 'https://www.perekrestok.ru/cat'
    url1 = 'https://lavka.yandex.ru/43/'

    try:
        driver.get(url=url)
        driver.implicitly_wait(6)
        sleep(1)


        driver.find_element_by_xpath('/html/body/div[1]/div/header/div[1]/div[1]/div[2]/div/button').click()
        sleep(2)


        address_string = driver.find_element_by_class_name('react-select__input').find_element_by_id(
            'react-select-2-input')
        sleep(2)

        address_string.send_keys(Keys.LEFT_CONTROL + 'a')  # удаляем если вдруг что-то лишнее в адресной строке имеется
        address_string.send_keys(Keys.BACKSPACE)  # удаляем если вдруг что-то лишнее в адресной строке имеется
        sleep(3)

        address_string.send_keys('г Казань, ул ' + these_keys[0] + ' ' + these_keys[1] + ' ,д ' + these_keys[2])
        sleep(2)

        address_string.send_keys(Keys.ENTER)
        sleep(4)

        pricee = driver.find_element_by_class_name('delivery-status__cost').text
        sleep(2)

        time_dostavki_perekrestok = driver.find_element_by_class_name('delivery-status__operation-time').text
        sleep(3)

        address_string.send_keys(Keys.ENTER)
        sleep(1)

        driver.get(url=url1)

        driver.find_element_by_xpath("/html/body/div/header/div[4]/button").click()  # четвертый div. copy full xpath

        address_string = driver.find_element_by_class_name('i164506l')
        sleep(2)
        address_string.send_keys(Keys.LEFT_CONTROL + 'a')
        sleep(1)
        address_string.send_keys('Россия, Республика Татарстан, Казань, ' + str(address))
        sleep(1)
        address_string.send_keys(Keys.SPACE)
        sleep(1)
        driver.find_element_by_class_name('l1xltboq').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button').click()
        sleep(2)

        driver.find_element_by_xpath('/html/body/div/header/div[5]/button').click()
        sleep(2)

        price_dostavki = driver.find_element_by_css_selector('body > div:nth-child(11) > div:nth-child(3) > div > div > div > ul > li:nth-child(2) > div.i1rcibxk > span:nth-child(1)').text # доставка от 1 рубля
        price_dostavki2 = driver.find_element_by_css_selector('body > div:nth-child(11) > div:nth-child(3) > div > div > div > ul > li:nth-child(3) > div > span:nth-child(1)').text #доставка от 0 рублей
        time_dostavki = driver.find_element_by_css_selector('body > div:nth-child(11) > div:nth-child(3) > div > div > div > ul > li:nth-child(1) > div.i1rcibxk > span:nth-child(2)').text
        price_dostavki3 = driver.find_element_by_css_selector('body > div:nth-child(11) > div:nth-child(3) > div > div > div > ul > li:nth-child(3) > div > span:nth-child(2)').text

        print(f'В Перекрестке {pricee}, Время: {time_dostavki_perekrestok}''\n'
              f'В Яндекс Лавке {price_dostavki} при заказе от 0 рублей и {price_dostavki2} при заказе от {price_dostavki3}, Время доставки: {time_dostavki}''\n'
              f'В Метро Стоимость доставки 189 Р, Время: в течение часа')

    except Exception:
        return 'Доставка по вашему адресу отсутствует'

    driver.close()
    driver.quit()


if __name__ == '__main__':
    Dostavka('Академика Парина 4')


import datetime
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver
from decimal import Decimal
from work_with_bd import add_to_db


def collect_url(url, region):
    driver = undetected_chromedriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(url=url)
        n = 0
        while True:
            try:
                if n == 5:
                    driver.refresh()
                if n == 10:
                    break
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_93444fe79c--wrapper--W0WqH")))
                print("Страница загружена")
                break
            except:
                print("Загрузка...")
                n += 1
                continue
        time.sleep(2)

        page_number = 1
        last_page = False

        while True:
            full_block = driver.find_element(By.CLASS_NAME, "_93444fe79c--wrapper--W0WqH")
            blocks = full_block.find_elements(By.CLASS_NAME, "_93444fe79c--container--Povoi._93444fe79c--cont--OzgVc")
            list_urls = []
            for item in blocks:
                find_href = item.find_element(By.CLASS_NAME, "_93444fe79c--link--eoxce")
                href = find_href.get_attribute("href")
                list_urls.append(href)
            with open(f"{datetime.date.today()}-{region}.txt", "a", encoding="utf-8") as file:
                for i in list_urls:
                    file.write(f"{i}\n")
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.switch_to.window(original_window)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if url == "https://novosibirsk.cian.ru/kupit-kvartiru-novostroyki/":
                url2 = f"https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p={1 + page_number}&region=4897"
            if url == "https://novosibirsk.cian.ru/kupit-kvartiru-vtorichka/":
                url2 = f"https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p={1 + page_number}&region=4897"
            if url == "https://spb.cian.ru/kupit-kvartiru-novostroyki/":
                url2 = f"https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p={1 + page_number}&region=2"
            if url == "https://spb.cian.ru/kupit-kvartiru-vtorichka/":
                url2 = f"https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p={1 + page_number}&region=2"
            try:
                driver.get(url2)
                time.sleep(1)
            except:
                continue
            page_number += 1
            if driver.current_url == "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p=1&region=4897" \
                    or driver.current_url == "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=1&region=4897":
                last_page = True
            if driver.current_url == "https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p=1&region=2" \
                    or driver.current_url == "https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=1&region=2":
                last_page = True
            if last_page:
                print("Last page")
                break
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_data(name_file):
    with open(f"{name_file}.txt", encoding="utf-8") as file:
        list_position = file.read().splitlines()
    for url in list_position:
        try:
            with requests.Session() as connection:
                connection.headers.update(
                    {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                        "accept": "accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    }
                )

                response = connection.get(url)
                print(response.status_code)
                time.sleep(1)
                soup = BeautifulSoup(response.text, "lxml")

                for_object = {}
                for_house = {}

                # price
                block_with_price = soup.find("span", class_="a10a3f92e9--price_value--lqIK0")
                block_with_price2 = block_with_price.find("span")
                price = block_with_price2.get("content")[:-2].replace(' ', '')
                for_object["price"] = int(price)

                general_block = soup.find("div", class_="a10a3f92e9--info-block--kXrDj")

                # total_area
                block_with_total_area = general_block.find("div", class_="a10a3f92e9--info-value--bm3DC")
                total_area = block_with_total_area.string.split()
                for_object["total_area"] = Decimal(total_area[0].replace(',', '.'))
                # for_object["total_area"] = total_area[0]

                # floor_num
                block_with_floors_num_title = general_block.find_all("div", class_="a10a3f92e9--info-title--JWtIm")
                index_title = 0
                for item in block_with_floors_num_title:
                    if item.string == "Этаж":
                        index_title = block_with_floors_num_title.index(item)
                        break
                block_with_floors_num = general_block.find_all("div", class_="a10a3f92e9--info-value--bm3DC")
                floor_num = block_with_floors_num[index_title].string.split(' ')
                for_object["floor_num"] = int(floor_num[0])

                # floors_count
                floors_count = block_with_floors_num[index_title].string.split(' ')
                for_house["floors_count"] = int(floors_count[-1])

                # category
                if soup.find("div",
                             class_="a10a3f92e9--button--OUjNH a10a3f92e9--offer_card_page-bti--spgEZ a10a3f92e9--collapsed-block-header--YjVTc "
                                    "a10a3f92e9--offer_card_block--no-margin--Qa9YL a10a3f92e9--offer_card_block--no-borderradius--xJTgJ"):
                    category = "newBuildingFlatSale"
                else:
                    category = "flatSale"
                for_object["category"] = category

                # offer_id
                offer_id = url.split('/')
                for_object["offer_id"] = int(offer_id[-2])

                # address
                geo = soup.find("div", class_="a10a3f92e9--geo--VTC9X")
                geo2 = geo.find("span")
                address = geo2.get("content")
                for_house["address"] = address

                # location
                location = address.split(',')[1]
                for_house["location"] = location

                # year_house
                if soup.find("span", class_="a10a3f92e9--status--PGvAt"):
                    year_house = soup.find("span", class_="a10a3f92e9--status--PGvAt")
                    for_house["year_house"] = int(year_house.string.split()[-1])
                else:
                    for_house["year_house"] = 0

                # url house
                if soup.find("a", class_="a10a3f92e9--link--ulbh5 a10a3f92e9--link--hZEYa"):
                    url_house = soup.find("a", class_="a10a3f92e9--link--ulbh5 a10a3f92e9--link--hZEYa").get("href")

                    response = connection.get(url_house)
                    print(response.status_code)
                    soup = BeautifulSoup(response.text, "lxml")

                    # house_material_type
                    if soup.find_all("div", class_="_7a3fb80146--text--EL3wJ"):
                        text = soup.find_all("div", class_="_7a3fb80146--text--EL3wJ")
                        index_text = 0
                        for item in text:
                            span = item.find("span")
                            if span.string == "Тип дома":
                                index_text = text.index(item)
                                break
                        value = soup.find_all("div", class_="_7a3fb80146--value--wcB9F")
                        house_material_type = value[index_text].string
                        for_house["house_material_type"] = house_material_type
                    elif soup.find_all("div", class_="_02712f2b3b--text--EL3wJ"):
                        text = soup.find_all("div", class_="_02712f2b3b--text--EL3wJ")
                        index_text = 0
                        for item in text:
                            span = item.find("span")
                            if span.string == "Тип дома":
                                index_text = text.index(item)
                                break
                        value = soup.find_all("div", class_="_02712f2b3b--value--wcB9F")
                        house_material_type = value[index_text].string
                        for_house["house_material_type"] = house_material_type
                else:
                    for_house["house_material_type"] = "unknown"
                add_to_db(for_object, for_house)
        except:
            continue


def main():
    while True:
        print("Введите 1 для сбора списка urls объявлений, список будет сохранен в файл с текущей датой")
        print("Введите 2 для заполнения БД из объвляений, добавленных в список urls")
        answer = input()
        if answer == "1":
            while True:
                print("Выберите регион:")
                print("Введите 1 для выбора Новосибирска, 2 для Санкт-Петербурга")
                answer2 = input()
                if answer2 == "1":
                    region = "nsk"
                    collect_url("https://novosibirsk.cian.ru/kupit-kvartiru-novostroyki/", region)
                    collect_url("https://novosibirsk.cian.ru/kupit-kvartiru-vtorichka/", region)
                    break
                if answer2 == "2":
                    region = "spb"
                    collect_url("https://spb.cian.ru/kupit-kvartiru-novostroyki/", region)
                    collect_url("https://spb.cian.ru/kupit-kvartiru-vtorichka/", region)
                    break
            break
        if answer == "2":
            while True:
                print(
                    "Введите название файла без расширения со списком urls. Файл должен находиться в той же папке, что и main.py")
                name_file = input()
                if name_file.split('.')[-1] == "txt":
                    print("Название необходимо ввести без расширения")
                if name_file:
                    get_data(name_file)
                    break
            break


if __name__ == "__main__":
    main()

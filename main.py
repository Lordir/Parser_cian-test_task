import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver


def collect_url(url, last_page):
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
        if driver.current_url == "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p=1&region=4897" \
                or driver.current_url == "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=1&region=4897":
            if last_page[0]:
                last_page[1] = True
            last_page[0] = True
            print("last page")
        if last_page[1]:
            print("last")
            driver.close()
            driver.quit()
            return last_page
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    # url = "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=2&region=4897"
    page_number = 0
    last_page = [False, False]
    while True:
        if last_page[1]:
            break
        print(last_page[1])
        url = f"https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p={page_number + 1}&region=4897"
        try:
            collect_url(url, last_page)
            page_number += 1
        except:
            continue
    page_number2 = 0
    last_page = [False, False]
    while True:
        if last_page[1]:
            break
        url = f"https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p={page_number2 + 1}&region=4897"
        try:
            collect_url(url, last_page)
            page_number2 += 1
        except:
            continue
    # https://novosibirsk.cian.ru/kupit-kvartiru/


if __name__ == "__main__":
    main()

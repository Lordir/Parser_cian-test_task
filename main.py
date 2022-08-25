import datetime
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver


def collect_url(url):
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
                with open(f"{datetime.date.today()}.txt", "a", encoding="utf-8") as file:
                    file.write((list_urls[item in list_urls]) + '\n')
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.switch_to.window(original_window)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if url == "https://novosibirsk.cian.ru/kupit-kvartiru-novostroyki/":
                url2 = f"https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p={1 + page_number}&region=4897"
            if url == "https://novosibirsk.cian.ru/kupit-kvartiru-vtorichka/":
                url2 = f"https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p={1 + page_number}&region=4897"
            driver.get(url2)
            time.sleep(1)
            page_number += 1
            if driver.current_url == "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&p=1&region=4897" \
                    or driver.current_url == "https://novosibirsk.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=1&region=4897":
                last_page = True
            if last_page:
                print("Last page")
                break
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    collect_url("https://novosibirsk.cian.ru/kupit-kvartiru-novostroyki/")

    collect_url("https://novosibirsk.cian.ru/kupit-kvartiru-vtorichka/")

    # https://novosibirsk.cian.ru/kupit-kvartiru/


if __name__ == "__main__":
    main()

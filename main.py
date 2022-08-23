import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pickle

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
options.add_argument(
    "accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(executable_path="D:\\Git\\Parser_cian-test_task\\chromedriver.exe")


def collect_url(url):
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    while True:
        try:
            driver.get(url=url)
            driver.implicitly_wait(5)
            for cookie in pickle.load(open("cookies", "rb")):
                driver.add_cookie(cookie)
            driver.implicitly_wait(1)
            driver.refresh()
            full_block = driver.find_element(By.CLASS_NAME, "_93444fe79c--wrapper--W0WqH")
            blocks = full_block.find_elements(By.CLASS_NAME, "_93444fe79c--container--Povoi._93444fe79c--cont--OzgVc")
            for item in blocks:
                find_href = item.find_element(By.CLASS_NAME, "_93444fe79c--link--eoxce")
                href = find_href.get_attribute("href")
                print(href)

            pagination = driver.find_elements(By.CLASS_NAME, "_93444fe79c--list-item--FFjMz")
            print(len(pagination))
            n = 0
            gg = []
            for page in pagination:
                print(page.text)
                if n != len(pagination):
                    try:
                        find_next_url = page.find_element(By.CLASS_NAME, "_93444fe79c--list-itemLink--BU9w6")
                        next_url = find_next_url.get_attribute("href")
                        print(next_url)
                        n += 1
                        gg.append(find_next_url)

                    except:
                        if n == len(pagination) - 1:
                            print("Конец")
                            driver.close()
                            driver.quit()
                        n = len(pagination) - 1
                        continue
                else:
                    break
            print(gg[0].text)
            actions = ActionChains(driver)
            actions.move_to_element(gg[0]).perform()
            time.sleep(2)
            gg[0].click()
            driver.implicitly_wait(10)
        # collect_url(gg[0])
        # find_next_url.click()
        # driver.implicitly_wait(2)
        # time.sleep(1)

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    # with requests.Session() as connection:
    #     connection.headers.update(
    #         {
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    #         }
    #     )
    #     response = connection.get(url=url)
    #     print(response.status_code)
    #
    #     soup = BeautifulSoup(response.text, "lxml")
    #
    #     full_block = soup.find("div", class_="_93444fe79c--wrapper--W0WqH")
    #     blocks = full_block.find_all("article", class_="_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc")
    #     for item in blocks:
    #         find_href = item.find("a", class_="_93444fe79c--link--eoxce")
    #         href = find_href.get("href")
    #         # print(href)
    #
    #     pagination = soup.find("div", class_="_93444fe79c--wrapper--bKcEk")
    #     pages = pagination.find_all("li", class_="_93444fe79c--list-item--FFjMz")
    #     next_page = pages[1].find("a", class_="_93444fe79c--list-itemLink--BU9w6")
    #     next_page_url = next_page.get("href")
    #
    #     print(next_page_url)
    #     collect_url(next_page_url)


def test(url):
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    try:
        driver.get(url=url)
        time.sleep(15)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    url = "https://novosibirsk.cian.ru/kupit-kvartiru/"
    # https://novosibirsk.cian.ru/kupit-kvartiru/
    collect_url(url)
    # test(url)


if __name__ == "__main__":
    main()

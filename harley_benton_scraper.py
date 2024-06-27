from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://harleybenton.com/electric-basses/?page=2"

chrome_options = Options()
chrome_options.add_argument("--headless")  
cards = []

def hb_scraper(url):
    
    driver = None
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "products__title"))
        )

        products = driver.find_elements(By.CLASS_NAME, "products__title")

        for product in products:
            anchor = product.find_element(By.TAG_NAME, "a")
            model = product.text
            link = anchor.get_attribute("href")

            bass_page_req = requests.get(link)
            bass_desc_page = BeautifulSoup(bass_page_req.text, "html.parser")
            description =  bass_desc_page.find("div", class_="container product-specifications")
            description = description.find_all("li")
            desc_list = {description.text.strip().split(":")[0] : description.text.strip().split(":")[1] for description in description if len(description.text.strip().split(":")) > 1}
            desc_list["link"] = link
            desc_list["model"] = model
            
            button = bass_desc_page.find("a", class_="button button--outlined--orange is-fullwidth has-margin-bottom-md", href = True)
            price_link = button["href"]
            time.sleep(5)
            price_page_req = requests.get(price_link)
            price_page = BeautifulSoup(price_page_req.text, "html.parser")
            price = price_page.find("div", "price fx-text fx-text--no-margin").text[2:]
            
            desc_list["price"] = price
            card= pd.Series(desc_list)
            cards.append(card)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

def main():
    
    for request in range(1,6):
        if request > 1:
            hb_scraper(URL + f"?page={request}")
        else:
            hb_scraper(URL)
    
    os.makedirs("HB", exist_ok= True)
    pd.DataFrame(cards).to_excel("HB/HBCatalog.xlsx")
    pd.DataFrame(cards).to_csv("HB/HBCatalog.csv")
    
if __name__ == "__main__":
    main()

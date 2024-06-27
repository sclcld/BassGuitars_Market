from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = "https://www.fender.com/it-IT/electric-basses/?start=0&sz=72"
URL2 = "https://www.fender.com/it-IT/bassi-elettrici-squier/?start=0&sz=48"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
fender_cards = []
squier_cards = []

def fender_scraper(url, mode):
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-tile-image"))
        )
        products = driver.find_elements(By.CLASS_NAME, "product-tile-image")   
        
        for product in products:

            link = product.get_attribute("href")
            page_request = requests.get(link)
            spec_page = BeautifulSoup(page_request.text, "html.parser")
            product_name = spec_page.find("h1", class_= "product-name").text
            price = spec_page.find("span", class_= "value").text.strip()
            spec = spec_page.find_all("li", class_="spec-attribute d-flex align-items-center")
            specs_list = {}
            specs_list["Product Name"]= product_name
            specs_list["Price"]= price
            for specs in spec:
                
                label= specs.find("div", class_= "label")
                value= specs.find("div", class_= "value") 
                specs_list[label.text.strip()]= value.text.strip()
            card= pd.Series(specs_list)
            print(card)
            if mode == "f":
                fender_cards.append(card)
            else:
                squier_cards.append(card)
        if mode == "f":
            pd.DataFrame(fender_cards).to_excel("Fender/Fender_Catalog.xlsx")
            pd.DataFrame(fender_cards).to_csv("Fender/Fender_Catalog.csv")
        else:
            os.makedirs("Squier", exist_ok= True)   
            pd.DataFrame(squier_cards).to_excel("Squier/Squier_Catalog.xlsx")
            pd.DataFrame(squier_cards).to_csv("Squier/Squier_Catalog.csv")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

def main():
    
    fender_scraper(URL, "f")
    fender_scraper(URL2, "s")

if __name__ == "__main__":
    main()


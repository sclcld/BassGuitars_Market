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
import os

URL = "https://www.schecterguitars.com/bass/4-string?page="

chrome_options = Options()
chrome_options.add_argument("--headless")
cards= []

def schechter_scraper(url):
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "facets-item-cell-grid-link-image"))
        )
        products_links = driver.find_elements(By.CLASS_NAME, "facets-item-cell-grid-link-image") 
        products_links= [product.get_attribute("href") for product in products_links if product]
        print(len(products_links))
        for link in products_links:
            card= {}
            spec_req= requests.get(link)
            
            page= BeautifulSoup(spec_req.text, "html.parser")
            product_name= page.find("h1", class_= "product-details-full-content-header-title")
            product_price= page.find("span", class_= "product-views-price-lead")
            if all((product_name, product_price)):
                card["Product Name"] = product_name.text
                card["Price"]= product_price.text
                specs_left= page.find_all("div", class_="product-fields-title col-sm-4 col-xs-12")
                specs_right= page.find_all("div", class_="product-field-text col-sm-8 col-xs-12")
                for index in range(len(specs_left)):
                    card[specs_left[index].text.strip()]= specs_right[index].text.strip()
                
                card= pd.Series(card)
                cards.append(card)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()    

def main():

    for page_num in range(1,4):
        schechter_scraper(URL + str(page_num))
    os.makedirs("Schechter")
    pd.DataFrame(cards).to_excel("Raw/Schechter/Schechter_Catalog.xlsx")
    pd.DataFrame(cards).to_csv("Raw/Schechter/Schechter_Catalog.csv")
   
if __name__ == "__main__":
    main()

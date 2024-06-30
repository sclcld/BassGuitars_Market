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

DIMARZIO= [
            "https://www.dimarzio.com/pickups/bass/jazz-bass-hum-canceling",
            "https://www.dimarzio.com/pickups/bass/p-bass-hum-canceling",
            "https://www.dimarzio.com/pickups/bass/p-bass-hum-canceling",
            "https://www.dimarzio.com/pickups/bass/other-bass",
            "https://www.dimarzio.com/pickups/pj-bass-set/relentless-pj-pair"
          ]
EMG = [
       "https://www.emgpickups.com/bass.html",
       "https://www.emgpickups.com/bass.html?p=2"
      ]               

BARTOLINI= [
            "https://bartolini.net/application/j/",
            "https://bartolini.net/application/pb4/",
            "https://bartolini.net/application/mm4/",
            "https://bartolini.net/application/bb/",
            "https://bartolini.net/application/x44/",
            "https://bartolini.net/product-category/bass-pickups/pj-bass/",
            "https://bartolini.net/product-category/bass-pickups/vintage-brand/"
           ]

AGUILAR= [
          "https://aguilaramp.com/collections/pickups?page=1",
          "https://aguilaramp.com/collections/pickups?page=2"
          ]

picks_to_df= []

def dimarzio():
    
    for url in DIMARZIO:
        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        pick_up_links= page.find_all("a", class_="product-title text-uppercase", href= True)
        for link in pick_up_links:
            pick_url= link["href"]
            dim_url= "https://www.dimarzio.com"     
            product_name= pick_url[::-1][: pick_url[::-1].index("/")][::-1].replace("-", " ")
            pick_req= requests.get( dim_url + pick_url)
            pick_page= BeautifulSoup(pick_req.text, "html.parser")
            price= pick_page.find_all("div", class_="field--item")[2].text[1:]
            card= {"Manufacturer": "DiMarzio", "Product Name": product_name, "Price ($)": price}
            picks_to_df.append(card)

def emg():

    for url in EMG:
        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        product_links= page.find_all("a", class_="product-item-link", href= True)
        for sec_url in product_links:
            pickup_req= requests.get(sec_url["href"])
            pick_page= BeautifulSoup(pickup_req.text, "html.parser")
            pick_name= pick_page.find("span", class_="base").text
            if (pick_name[0] == "3", pick_name[0] == "4", pick_name[0] == "D",
                pick_name[0] == "F", pick_name[0] == "G", pick_name[0] == "J", 
                pick_name[0] == "M", pick_name[0] == "P", pick_name[0] == "R", 
                pick_name[0] == "T"):
                price= pick_page.find("span", class_="price").text[1:]
                card= {"Manufacturer": "Emg", "Product Name": pick_name, "Price ($)": price}
                picks_to_df.append(card)
    
def bartolini():
   
   def links_scraper():
        
        links= []
        for url in BARTOLINI:
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sb-divi-acf-table-image-item"))
                )       
                pick_cards= driver.find_elements(By.CLASS_NAME,"sb-divi-acf-table-image-item")
                for p in pick_cards:
                    pick_url = p.get_attribute("href")
                    links.append(pick_url)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                driver.quit()

            return links         
   
        pickups= {}
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        links= links_scraper()
        for link in links:
            driver.get(link)
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product_title.entry-title"))
                )
            name= driver.find_element(By.CSS_SELECTOR, ".product_title.entry-title").text
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
                )
            price= driver.find_element(By.CLASS_NAME, "price").text
            pickups[name]= price
        pickups= pd.Series(pickups, name= "Bartolini Pickups")
        pickups.to_csv("Raw/Pickups/bartoliniPickups.csv")

def aguilar():
        
        for url in AGUILAR:
            req= requests.get(url)
            page= BeautifulSoup(req.text, "html.parser")
            products= page.find_all("li", class_= "grid__item")
            for x in products:
                name= x.find("a", class_="full-unstyled-link", href= True).text.strip()[7:]
                price= x.find("span", class_="price-item price-item--regular").text.strip()[1:-4]
                card= {"Manufacturer": "Aguilar", "Product Name": name, "Price ($)": price}
                picks_to_df.append(card)

def main():
        
        dimarzio()
        emg()       
        bartolini()
        aguilar()
        os.makedirs("Raw2/Pickups")
        pd.DataFrame(picks_to_df).to_excel("Raw2/Pickups/pickups.xlsx")
    
if __name__ == "__main__":
    main()

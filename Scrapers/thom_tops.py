from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os

URL= "https://www.thomann.de/it/topseller_GF_bassi_elettrici.html"

chrome_options = Options()
chrome_options.add_argument("--headless")
manufacturer= []
model= []
price= []
ratings= []
rev_num= []

def tops_scraper():

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fx-ranked-product"))
        )
        products = driver.find_elements(By.CLASS_NAME, "fx-ranked-product")
        for product in products:
            manufacturer.append(product.find_element(By.CLASS_NAME, "fx-ranked-product__title-manufacturer").text.strip())
            model.append(product.find_element(By.CLASS_NAME, "fx-ranked-product__title-name").text.strip())
            price.append(product.find_element(By.CLASS_NAME, "fx-ranked-product__price").text.replace("€", "").replace(".",""))
            rating= product.find_element(By.CLASS_NAME, "fx-rating-stars__filler").get_attribute("style").split()[1].strip()[:-2]
            rating= round((float(rating) / 100)  * 4 + 1, ndigits=1)
            ratings.append(rating)
            sold= product.find_element(By.CLASS_NAME, "fx-rating-stars").text
            rev_num.append(sold)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
    



def main():
    
    tops_scraper()
    df= pd.DataFrame()
    df["Product Name"]= model
    df["Manufacturer"]= manufacturer
    df["Price"]= price
    df["Ratings"]= ratings
    df["Sold"]= rev_num
    print(os.getcwd())
    path = "C:\\Users\\pc\\MarABass\\Clean"
    os.chdir(path)
    df.to_excel("thomann_topsellers.xlsx")

if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

THOM= "https://www.thomann.de/it/tutti-i-prodotti-della-categoria-bassi-elettrici.html?ls=100&pg=1"

def star_counter(stars):

    mean= 0
    leg= {
            "star-full": 1,
            "star-half": 0.5,
            "star-empty": 0
        }
    for star in stars:
        current_star= star["class"][2]
        mean += leg[current_star]
    return mean    

def strumenti_musicali():

    urls= [
           "https://www.strumentimusicali.net/default.php/cPath/235_666_26/bassi-elettrici/bassi-jazz-style-4-corde.html",
           "https://www.strumentimusicali.net/default.php/cPath/235_666_26/bassi-elettrici/bassi-jazz-style-4-corde.html/page/2",
           "https://www.strumentimusicali.net/default.php/cPath/235_666_26/bassi-elettrici/bassi-jazz-style-4-corde.html/page/3",
           "https://www.strumentimusicali.net/default.php/cPath/235_666_26/bassi-elettrici/bassi-jazz-style-4-corde.html/page/4",
           "https://www.strumentimusicali.net/default.php/cPath/235_666_26/bassi-elettrici/bassi-jazz-style-4-corde.html/page/5",
           "https://www.strumentimusicali.net/default.php/cPath/235_666_26/bassi-elettrici/bassi-jazz-style-4-corde.html/page/6"
        ]
    data= []
    for url in urls:
        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        cards= page.find_all("td", class_="productListing-data")
        for card in cards:
            if card:
                name= card.find("b", class_="listing_prod_name")
                if name:
                    name= name.text.strip()
                    stars= card.find_all("span")
                    price= stars[5].text
                    stars= stars[:5]
                    stars= star_counter(stars)
                    record= {"Product": name, "Price": price, "Reviews": stars}
                    data.append(record)
    pd.DataFrame(data).to_excel("Raw/Reviews/strumentimusicali_reviews.xlsx")

def thomann():           
    
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


    def rating_bar_scraper(rating_bar):

        try:
            total_reviews= rating_bar.find_element(By.CLASS_NAME, "fx-rating-stars__description").text
            star_div= rating_bar.find_element(By.CLASS_NAME, "fx-rating-stars__stars")
            star_div= star_div.find_elements(By.TAG_NAME, "use")
            filler_element = rating_bar.find_element(By.CLASS_NAME, "fx-rating-stars__filler")
            style_attribute = filler_element.get_attribute("style")
            style_attribute= int(style_attribute.split()[1][:-2])
            style_attribute_five_scale= (style_attribute / 100) * 4 + 1

            return style_attribute_five_scale, total_reviews

        except:
            
            return 0, 0        


    def scraper(url):
        
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product"))
            )
            products= driver.find_elements(By.CLASS_NAME, "product")   
            for product in products:
                name= product.find_element(By.CLASS_NAME, "title__name").text  
                manuf= product.find_element(By.CLASS_NAME, "title__manufacturer").text
                price= product.find_element(By.CSS_SELECTOR, ".fx-typography-price-primary.fx-price-group__primary.product__price-primary").text
                rating_bar= product.find_element(By.CLASS_NAME, "product__meta-line")
                ranking, total_reviews= rating_bar_scraper(rating_bar)
                product_card ={"Product name": name, 
                    "Manufacturer": manuf, 
                    "Price": price, 
                    "Ranking": ranking, 
                    "Total_Reviews":total_reviews
                    }
                data.append(product_card)
        except Exception as e:
            print(f"Error: {e}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    data= []
    
    for url in range(1,23):
        new_url= THOM[:-1]+ str(url)
        try:
            scraper(new_url)
        except Exception as e:
            print(f"Error: {e}")
    
    pd.DataFrame(data).to_excel("Raw/Reviews/thomann_reviews.xlsx")

    driver.quit()
   
    
def main():
    
    os.makedirs("Raw/Reviews", exist_ok= True)
    strumenti_musicali()
    thomann()

if __name__== "__main__":
    main()
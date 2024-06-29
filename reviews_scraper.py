import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

MERCATINO= "https://www.mercatinomusicale.com" 
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

def mercatino_musicale(url):
    print("here")

    req= requests.get(url)
    print(req)
    page= BeautifulSoup(req.text, "html.parser")
    print(page)
    link_button= page.find("a", class_="btn icon-angle-right", href= True)
    print(link_button)
    if not link_button :
        print("dis")
        return
    print("here")
    cards= page.find_all("div", class_="box_prod box_prod_sm box_prod_sm_2 box_prod_sm_6 box_prod_linked")
    for card in cards:
        product_links= card.find_all("a", class_= "box_prod_link", href= True)
        for c in product_links:
            bass_page_link= MERCATINO + c["href"]
            new_req= requests.get(bass_page_link)
            bass_page= BeautifulSoup(new_req.text, "html.parser")
            bass_desc_link= bass_page.find("a", class_="btn btn_fly btn_exturl", href= True)["href"]
            
            bass_desc_req= requests.get(bass_desc_link)
            bass_desc_page= BeautifulSoup(bass_desc_req.text, "html.parser")
            print(bass_desc_page.find("h1").text)
    
    new_url= MERCATINO + link_button["href"]
    print("\n\n\n\n\n")
    mercatino_musicale(new_url)

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
            print(total_reviews)
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
            print("driver ready")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product"))
            )
            print("page fully downloaded")
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
                print(product_card)
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
   
    # finally:
    #     driver.quit()    




    
def main():
    
    # os.makedirs("Raw/Reviews", exist_ok= True)
    # strumenti_musicali()
    #mercatino_musicale("https://www.mercatinomusicale.com/mm/s_bassi-elettrici-4-corde_rp3-ct29-gp1pc.html")
    thomann()

if __name__== "__main__":
    main()
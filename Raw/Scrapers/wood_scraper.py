import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def filbo():

    def scraper(url):
        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        links= page.find_all("a", class_="collection-list__link", href= True)
        products= {}
        for link in links :
            wood_req= requests.get("https://filbosnc.it" + link["href"])
            wood_page= BeautifulSoup(wood_req.text, "html.parser")
            wood= wood_page.find_all("div", class_="product-block grid__item one-quarter small-down--one-half")
            for w in wood:
                product_name= w.find("div", class_= "product-block__title").text
                price= w.find("div", class_= "product-price").text.replace("Da","").replace("Prezzo","").strip()
                products[product_name]= price
        
        return products
        
    bodies= "https://filbosnc.it/pages/body-per-elettrica"
    fretb= "https://filbosnc.it/pages/tastiere-per-bassi"

    os.makedirs("Raw/Woods/Filbo", exist_ok= True)    
    bodies= pd.Series(scraper(bodies), name= "Filbo Bodies").to_csv("Raw/Woods/Filbo/bodies.csv")
    fretb= pd.Series(scraper(fretb), name= "Filbo Fretb").to_csv("Raw/Woods/Filbo/fretbs.csv")


def rumore_legno():

    def scraper(url):

        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        products= {}
        wood= page.find_all("div", class_="post_content")
        
        for w in wood:
            p_name= w.find("a").text
            p_price= w.find("bdi").text
            products[p_name]= p_price

        return products            

    bodies= "https://www.rumorelegno.it/categoria-prodotto/basso/body-basso-elettrico/"
    fretbs=  "https://www.rumorelegno.it/categoria-prodotto/basso/tastiere-basso-elettrico/tastiere-4-corde/"
    necks= "https://www.rumorelegno.it/categoria-prodotto/basso/manico-basso-elettrico/manico-4-5-corde/"
    tops= "https://www.rumorelegno.it/categoria-prodotto/basso/top-basso-elettrico/"
    pcov= "https://www.rumorelegno.it/categoria-prodotto/basso/copripaletta/"

    os.makedirs("Raw/Woods/RumoreLegno")
    pd.Series(scraper(bodies)).to_csv("Raw/Woods/RumoreLegno/bodies.csv")
    pd.Series(scraper(fretbs)).to_csv("Raw/Woods/RumoreLegno/fretbs.csv")
    pd.Series(scraper(necks)).to_csv("Raw/Woods/RumoreLegno/necks.csv")
    pd.Series(scraper(tops)).to_csv("Raw/Woods/RumoreLegno/tops.csv")
    pd.Series(scraper(pcov)).to_csv("Raw/Woods/RumoreLegno/pcov.csv")

def tonewood():

    def scraper(url):

        print(url)
        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        products= page.find_all("div", class_="wpb_wrapper")
        print("here")
        for p in products:
        
            print(p.text)
            
    
    bodies= "https://www.tonewood.it/body-solidbody/"
    necks= "https://www.tonewood.it/manici/"
    fretboards= "https://www.tonewood.it/tastiere/"

    scraper(bodies)

def m2woods():

    bodies= "https://www.m2wood.com/shop/contents/it/d4.html"

def main():

    os.makedirs("Raw/Woods", exist_ok= True)
    filbo()
    rumore_legno()
    



if __name__ == "__main__":
    main()


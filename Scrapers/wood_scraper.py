import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

to_df= []

def filbo():

    def scraper(url):
        
        req= requests.get(url)
        
        page= BeautifulSoup(req.text, "html.parser")
        links= page.find_all("a", class_="collection-list__link", href= True)
        products= []
        for link in links :
            wood_req= requests.get("https://filbosnc.it" + link["href"])
            wood_page= BeautifulSoup(wood_req.text, "html.parser")
            wood= wood_page.find_all("div", class_="product-block grid__item one-quarter small-down--one-half")
            for w in wood:
                product_name= w.find("div", class_= "product-block__title").text
                price= w.find("div", class_= "product-price").text.replace("Da","").replace("Prezzo","").strip()[1:]
                product_name= product_name.lower().replace("basso","bassi").replace("bassi","-").replace("body", "body -")
                product_name= product_name.split()
                material= " ".join(product_name[1:]).replace("-", "").replace("promozione !!", "").replace("offerta","")
                product_type= product_name[0]
                pz= "1"
                cut_index = 0
                found= False
                if "°" not in material and "mm." not in material:
                    for letter_index in range(len(material)):
                        
                        if not found and material[letter_index].isnumeric() or material[letter_index] == "/":
                            found= True
                            cut_index= letter_index
                            pz=""
                        if found and material[letter_index].isnumeric() or material[letter_index] == "/":
                            pz += material[letter_index]
                if found:
                    material= material[:cut_index-1]
                card= {"Seller": "Filbo", "Item": product_type, "Material": material, "Price (€)": price, "Pieces": pz} 
                to_df.append(card)

                
        
        return products
        
    bodies= "https://filbosnc.it/pages/body-per-elettrica"
    fretb= "https://filbosnc.it/pages/tastiere-per-bassi"
    scraper(bodies)
    scraper(fretb)
    

def rumore_legno():

    def scraper(url):

        req= requests.get(url)
        page= BeautifulSoup(req.text, "html.parser")
        products= []
        wood= page.find_all("div", class_="post_content")
        
        for w in wood:
            p_name= w.find("a").text.replace("Copri Paletta", "CopriPaletta")
            p_price= w.find("bdi").text[1:].strip()
            pz= "1"
            product_type= p_name.split()[0]
            quantity= p_name.split()[-1]
            if "pz" in quantity:
                if len(quantity) == 3:
                    pz= quantity[0]
                else:
                    pz= p_name.split()[-2]
            material= " ".join(p_name.split()[1:-1])
            material= "".join([letter for letter in material if letter.isalpha() or letter.isspace()])
            card= {"Seller": "Rumore Legno", "Item": product_type, "Material": material, "Price (€)": p_price, "Pieces": pz}
            to_df.append(card)
           
        return products            

    bodies= "https://www.rumorelegno.it/categoria-prodotto/basso/body-basso-elettrico/"
    fretbs=  "https://www.rumorelegno.it/categoria-prodotto/basso/tastiere-basso-elettrico/tastiere-4-corde/"
    necks= "https://www.rumorelegno.it/categoria-prodotto/basso/manico-basso-elettrico/manico-4-5-corde/"
    tops= "https://www.rumorelegno.it/categoria-prodotto/basso/top-basso-elettrico/"
    pcov= "https://www.rumorelegno.it/categoria-prodotto/basso/copripaletta/"

    
    for product in (bodies, fretbs, necks, tops, pcov):

        scraper(product)

def main():

    filbo()
    rumore_legno()
    os.makedirs("Raw/Woods", exist_ok= True)
    pd.DataFrame(to_df).to_excel("Raw/Woods/Woods.xlsx")
    
    



if __name__ == "__main__":
    main()






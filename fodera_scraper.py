import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

START= "https://fodera.com"
URL= "https://fodera.com/collections/custom-instrument-deposit?view=view-36"
URL2= "https://fodera.com/collections/standard-instrument-deposit?page=1&view=view-36"

cards = []

def fodera_scraper(url):

    req= requests.get(url)
    page= BeautifulSoup(req.text, "html.parser")
    anchors= page.find_all("a", href= True)
    for anchor in anchors:
        
        anchor_url= anchor["href"]
        if len(anchor_url) > 50 and "collections" in anchor_url:
            spec_url= (START + anchor_url)
            spec_rec= requests.get(spec_url)
            page= BeautifulSoup(spec_rec.text, "html.parser")
            price= page.find("span", class_= "meta").text.strip()[1:]
            name= page.find("h1", class_= "product__title type-heading-1" or "product__description type-body-regular rte").text.strip()
            specs= page.find("div", class_= "product__details")
            specs= specs.find("ul")
            card= {}
            card["Product Name"]= name
            card["Price"]= price
            if specs:
                clean_specs= [spec.replace("w/", "").replace("\xa0", "") for spec in specs.text.strip().split("\n") if spec]
                
                for spec in clean_specs:
                    print(spec)
                    if "Body" in spec:
                        if all(("Fingerboard" in spec, "+$" not in spec)):
                            records = spec.split("/")
                            card["Body Material"] = records[0].replace("Body", "")
                            card["Fingerboard"] = records[1].replace("Fingerboard", "")
                        else:
                            card["Body Material"] = spec
                    elif "Top" in spec:
                        card["Top"]= spec
                    elif "Neck" in spec:
                        card["Neck"] = spec
                    elif "Fingerboard" in spec:
                        if any(("Ebony" in spec, "PLEK" in spec)):
                            card["Neck"]= spec.replace("Fingerboard", "")
                    elif "Frets" in spec:
                        splitted= spec.split("," if "," in spec else " ")
                        if len(splitted) == 2:
                            card["Frets"]= splitted[0]
                        elif len(splitted) == 3:
                            card["Frets"]= splitted[1].split()[0]
                        else:
                            card["Frets"]= splitted[0] 
                    elif all(("Fret" in spec, "Tulips" not in spec)):
                        splitted= spec.split(",")
                        print(splitted)
                        card["Frets"]= splitted[1].replace("-", " ").split()[0]
                    elif any(("Coil" in spec, "Pickup" in spec)) and "Spacing" not in spec:
                        if "[" in spec:
                            clean= spec[:spec.index("[")]
                        elif "(" in spec:
                            clean= spec[:spec.index("(")]    
                        else:
                            clean= spec    
                        card["Pickups"]= clean
            
            cards.append(pd.Series(card))
        

def main():
    
    fodera_scraper(URL)
    fodera_scraper(URL2)
    os.makedirs("Fodera", exist_ok= True)
    pd.DataFrame(cards).to_excel("Fodera/Fodera_Catalog.xlsx")
    pd.DataFrame(cards).to_csv("Fodera/Fodera_Catalog.csv")

if __name__ == "__main__":
    main()

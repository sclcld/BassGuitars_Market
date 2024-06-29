import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def bridge_scraper():
    
    hipshot= "https://hipshotproducts.com/collections/bass-bridges"
    abm1= "https://abm-guitarpartsshop.com/ABM-GUITAR-PARTS/Bass-Bridges/ABM-3700-MKII-Bass-Bridge/ABM-3704-MKII-4-String/Bell-Brass:::256_55_56_257_258.html"
    abm2= "https://abm-guitarpartsshop.com/ABM-GUITAR-PARTS/Bass-Bridges/ABM-3700-MKII-Bass-Bridge/ABM-3704-MKII-4-String/Aluminum:::256_55_56_257_259.html"
    babicz= "https://www.fullcontacthardware.com/fch-4-string-bass-bridge"
    kahler1= "https://kahlerusa.com/product/2440-series-professional-fixed-bass-bridge-system/"
    kahler2= "https://kahlerusa.com/product/7440-series-hybrid-fixed-bass-bridge-system/"

    products_dict= {}
    req= requests.get(hipshot)
    page= BeautifulSoup(req.text, "html.parser")
    products= page.find_all("a", class_="product-image", href= True)

    for product in products:
        url= "https://hipshotproducts.com" + product["href"]
        p_req= requests.get(url)
        b_page= BeautifulSoup(p_req.text, "html.parser")
        products = b_page.find_all("form", class_="form-vertical product-form product-form-product-template")
        for p in products:
            product_name = "Hipshot - " + p.find("h1").text
            price= p.find("span", class_= "money").text
            products_dict[product_name]= price
    
    for s_url in (abm1, abm2):
        abm_req= requests.get(s_url)
        abm_page= BeautifulSoup(abm_req.text, "html.parser")
        products= abm_page.find_all("a", class_="btn-details", href= True)
        for p in products:
            abm_burl= p["href"]
            b_req= requests.get(abm_burl)
            abm_bpage= BeautifulSoup(b_req.text, "html.parser")
            prods= abm_bpage.find_all("div", class_="pd_summarybox")
            for prod in prods:
                p_name= prod.find(attrs={"itemprop": "name"}).text
                p_price= prod.find("span", class_="new_price").text.replace("Jetzt nur  ", "").strip()
                products_dict[p_name]= p_price

    
    babicz_req= requests.get(babicz)
    babicz_page= BeautifulSoup(babicz_req.text, "html.parser")
    p_name= babicz_page.find("span", class_="h2").text
    prices= set(babicz_page.text.split("\n"))
    for line in prices:
        if "USD" in line:
            limit= line.index(" ")
            p_name = p_name.replace("original series,", "") + f" {line[:limit]}"
            p_price= line[limit:]
            products_dict[p_name]= p_price

    for url in (kahler1, kahler2):
        kahl_req= requests.get(url)
        kahl_page= BeautifulSoup(kahl_req.text, "html.parser")
        k_name= "Kahler - " + kahl_page.find("h1", class_="product_title entry-title").text
        k_price= kahl_page.find("p", class_="price").text
        products_dict[k_name]= k_price

    os.makedirs("Raw/Bridges")
    pd.Series(products_dict, name= "Bridges").to_csv("Raw/Bridges/bridges.csv")
bridge_scraper()
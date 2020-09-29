import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import csv 
import urllib.request

import os 
os.chdir("/Users/susanchen/Desktop/Korean_skin_care/Sokoglam")



def get_links(link):
    #prod = "https://sokoglam.com/collections/oily"
    prod_pg = requests.get(link)
    soup = BeautifulSoup(prod_pg.text, 'html.parser')
    block = soup.find_all("h2", class_= 'product__title')

    Links = []
    for link in block:
        l= link.find('a').get('href')
        Links.append('http://sokoglam.com'+l)

    return Links



def scrape(linkArray):
    for link in linkArray:
        productPage = requests.get(link)
        Soup = BeautifulSoup(productPage.text, 'html.parser')
        
        # extract product name 
        name = Soup.find('h1', class_ = 'pdp__product-title').text
        product_name.append(name)
        
        # extract brand name 
        b = Soup.find('h3', class_ = "pdp__product-vendor").text
        brand.append(b.strip())

        # extract product price 
        p = Soup.find('span', class_ = 'pdp__product-price')
        price.append(p.text.strip())

        # extract product ingredients
        try: 
            i = Soup.find('div',  class_ = 'tab-content--full').text.strip()
            ingredients.append(i)
        except AttributeError:
            ingredients.append('')

        # extract product description 
        try:
            description = Soup.find("div", class_='pdp-tab-content').text.strip()
            descriptions.append(description)
        except AttributeError:
            descriptions.append("")


    #get_num_reviews()
    #get_rating()
    #unable to extract rating and review

    data = {"Product": product_name, 'Brand': brand, 'Description': descriptions, "Ingredients": ingredients, 'Price': price}
    return data



def preclean(dataframe):
    for i in range(len(dataframe)):
        dataframe.Description[i] = dataframe.Description[i].replace('\n', '')
        dataframe.Price[i] = dataframe.Price[i].translate({ord('$'): None})
        dataframe.Ingredients[i] = dataframe.Ingredients[i].replace("Full List of Ingredients\n", '')
        dataframe.Ingredients[i] = dataframe.Ingredients[i].replace("Show Less", '')



def save(data, fileName):
    df = pd.DataFrame(data)
    preclean(df)
    df.to_csv(fileName + ".csv", index = False)


if __name__ == "__main__":

    ## Oily Collection 
    olinks = get_links("https://sokoglam.com/collections/oily")
    product_name = []
    brand =[]
    price = []
    ingredients = []
    descriptions = []
    oily_data = scrape(olinks)
    save(oily_data, 'oily')

    ## Dry Collection 
    dry_links= get_links("https://sokoglam.com/collections/dry") 
    product_name = []
    brand =[]
    price = []
    ingredients = []
    descriptions = []
    dry_data = scrape(dry_links)
    save(dry_data, 'dry')

    ## Combination Collection
    com_links = get_links("https://sokoglam.com/collections/combination")
    product_name = []
    brand =[]
    price = []
    ingredients = []
    descriptions = []
    com_data = scrape(com_links)
    save(com_data, 'combination')


    ## Normal Collection 
    norm_links = get_links("https://sokoglam.com/collections/normal")
    product_name = []
    brand =[]
    price = []
    ingredients = []
    descriptions = []
    norm_data = scrape(norm_links)
    save(norm_data, 'normal')
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 22:03:37 2020

@author: bubbl
"""

import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
from csv import reader


inputfile = r"C:\Users\bubbl\Documents\Work Stuff\Projects\compiled_links.csv"

# read csv file as a list of lists
with open(inputfile, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    urls = list(csv_reader)
    # print(urls)
flattened = [val for sublist in urls for val in sublist] 
# print(flattened)

dfs = []
for url in flattened: 
    sleep = (1)
    page = requests.get(url)
    soup = BS(page.content,"html.parser")
    
    uni_name = []
    address = []
    region = []
    locality = []
    postal = []
    country = []
    
    uni = soup.find ('h1')
    uni_name = uni.text
    
    add = soup.find('span', attrs={"itemprop":"streetAddress"})
    address = add.text   
    
    reg = soup.find('span', attrs={"itemprop":"addressRegion"})
    region = reg.text
    
    local = soup.find('span', attrs={"itemprop":"addressLocality"})
    # print(locality.get_text())
    locality = local.text
    
    pos = soup.find('span', attrs={"itemprop":"postalCode"})
    # print(postal.get_text())
    postal = pos.text
    
    ctry = (soup.find_all('span', attrs={"itemprop":"name"}))[2]
    country = ctry.text
    
    uni.append(uni_name)
    add.append(address)
    reg.append(region)
    local.append(locality)
    pos.append(postal)
    
    df = pd.DataFrame(
        {'University': [uni_name],
         'Address': [address],
         'State': [region],
         'Town': [locality],
         'Postal': [postal],
         'Country': [country]
        })
    dfs.append(df)
    
df_fin = pd.concat(dfs, ignore_index=True)
df_fin.to_csv('output1.csv', index=False, encoding='utf-8')


# =============================================================================
# # df = pd.DataFrame(columns=['name','region','locality','postal'])
# # print(df)
# 
# url = "https://www.4icu.org/reviews/9107.htm"
# 
# 
# page = requests.get(url)
# page.text
# soup = BS(page.content,"html.parser")
# =============================================================================


# =============================================================================
# uni = []
# uni_elem = soup.find ('h1')
# for item in uni_elem:
#     uni.append(uni_elem.text)
#     
# address = []
# address_elem = soup.find('span', attrs={"itemprop":"streetAddress"})
# for item in address_elem:
#     address.append(address_elem.text)  
# 
# region = []
# region_elem = soup.find('span', attrs={"itemprop":"addressRegion"})
# # print(region.get_text())
# for item in region_elem:
#     region.append(address_elem.text)
# 
# locality = []
# locality_elem = soup.find('span', attrs={"itemprop":"addressLocality"})
# # print(locality.get_text())
# for item in locality_elem:
#     locality.append(locality_elem.text)
# 
# postal = []
# postal_elem = soup.find('span', attrs={"itemprop":"postalCode"})
# # print(postal.get_text())
# for item in postal_elem:
#     postal.append(postal_elem.text)
# 
# unitown_list = pd.DataFrame(
#     {'University': uni,
#      'Address': address,
#      'State': region,
#      'Town': locality,
#      'Postal': postal
#     })
# print(unitown_list)
# =============================================================================



# =============================================================================
# def uni_list(url): 
#     page = requests.get(url)
#     page.text
#     soup = BS(page.content,"html.parser")
    
#     # to get the uni name
#     uni = []
#     uni_elem = soup.find ('h1')
#     #print(uni.get_text())
#     for item in uni_elem:
#         uni.append(item.text.replace("\n"," "))
    
#     # to get the address
#     address = []
#     address_elem = soup.find('span', attrs={"itemprop":"streetAddress"})
#     # print(address.get_text())
#     for item in address_elem:
#         address.append(item.text.replace("\n"," "))
    
#     region = []
#     region_elem = soup.find('span', attrs={"itemprop":"addressRegion"})
#     # print(region.get_text())
#     for item in region_elem:
#         region.append(item.text.replace("\n"," "))
    
#     locality = []
#     locality_elem = soup.find('span', attrs={"itemprop":"addressLocality"})
#     # print(locality.get_text())
#     for item in locality_elem:
#         locality.append(item.text.replace("\n"," "))
    
#     postal = []
#     postal_elem = soup.find('span', attrs={"itemprop":"postalCode"})
#     # print(postal.get_text())
#     for item in postal_elem:
#         postal.append(item.text.replace("\n"," "))
    
#     #create dataframe
#     unitown_array = []

#     for uni, address, region, locality, postal in zip(uni, address, region, locality, postal):
#         unitown_array.append({'University': uni, 'Street': address, 'State': region, 'Town': locality, 'Postal': postal})

#     return unitown_array
# =============================================================================

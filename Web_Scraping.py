import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

path = 'C://Users/bubbl/Documents/test/'

#index 2(A) to 27(Z)
file = []
for i in range(2,28):
    #print(i)
    url = "https://www.4icu.org/reviews/index" + str(i) + ".htm"
    response = requests.get(url)
    soup = BS(response.text,"html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True)]
    #print(links)
    
    file.append(links)
    
df = pd.DataFrame(file)
cols = list(range(0,64))
df2 = df.copy()
df2.drop(df2.columns[cols], axis = 1, inplace = True)
df2 = pd.melt(df2).dropna()
df2 = df2[df2['value'].str.contains('/reviews/')]
df2.drop(df2.columns[0], axis =1, inplace=True)

df2.to_csv(path + 'links.csv', header=False, index=False, encoding='utf-8', line_terminator='\r')


from csv import reader

inputfile = path + "links.csv"

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
    page = requests.get("https://www.4icu.org" + url)
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
df_fin.to_csv(path+'output.csv', index=False, encoding='utf-8')

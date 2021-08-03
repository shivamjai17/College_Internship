import requests
from bs4 import BeautifulSoup
import pandas as pd

name=[]
price=[]
MRP=[]
Save=[]
imglink=[]

for i in range(2,20):
    url='https://www.amazon.in/s?k=LG'
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    item=soup.find_all('div',attrs={'data-component-type':'s-search-result'})
    for i in item:
        a=i.find('span',attrs={'class':"a-size-medium a-color-base a-text-normal"})

        name.append(a.text)
        b=i.find('span',attrs={'class':"a-price-whole"})
        if b:
            price.append(b.text)
        else:
            pass
        c=i.find('span',attrs={'class':"a-price-whole"})
        if c:
            MRP.append(c.text)
        else:
            pass
        d=i.find('span',attrs={'class':"a-size-base"})
        if d:
            Save.append(d.text)
        else:
            pass
        e=i.find('img',attrs={'class':"s-image"})
        imglink.append(e.get('src'))
print(len(name))
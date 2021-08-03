from logging import debug
from types import MethodType
from flask import Flask, render_template, redirect,request,session,url_for
from numpy.core.fromnumeric import product

import requests
from bs4 import BeautifulSoup
import pandas as pd


app = Flask(__name__)
@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/hello/<string:productName>')
def hello(productName):
  
    productName = request.args.get('q')
    
    htmlSourceCode = gethtml(productName)
    
    soup=BeautifulSoup(htmlSourceCode,'html.parser')
    a_tags = soup.find_all('a',{'class':'s1Q9rs'})
    
    urls = list()
    
    for a in soup.find_all('a',{'class':'s1Q9rs'}):
        urls.append('https://www.flipkart.com'+a['href'])
        
    for a in soup.find_all('a',{'class':'_1fQZEK'}):
        urls.append('https://www.flipkart.com'+a['href'])
        
    
    for a in soup.find_all('a',{'class':'_2UzuFa'}):
        urls.append('https://www.flipkart.com'+a['href'])
        
    name=[]
    MRP=[]    
    RetRew=[]
    Ratting=[]
    off=[]
    for url in urls:
        page_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        try:
            title = page_soup.find('h1', {'class':'yhB1nd'})
            
        except:
            title = page_soup.find('span', {'class':'B_NuCI'})
        name.append(title.text)

        price = page_soup.find('div',attrs={'class':"_30jeq3 _16Jk6d"})
        MRP.append(price.text)
        try:
            ratrew = page_soup.find('span',attrs={'class':"_2_R_DZ"}) 
            RetRew.append( ratrew.text)
        except:
            ratrew = page_soup.find('div',attrs={'class':"_3LWZlK"})
            RetRew.append( ratrew.text)
      
        rat=page_soup.find('div',attrs={'class':"_3LWZlK"})
        Ratting.append(rat.text)
        # try:
        #     offer=page_soup.find('div',attrs={'class':"_3Ay6Sb _31Dcoz"})
        #     off.append(offer.text)
        # except:
        #     offer=page_soup.find('div',attrs={'class':"_3Ay6Sb _31Dcoz pZkvcx"})
        #     off.append(offer.text)
        
    product={
        'title':name,
        'MRP':MRP,
        'Rating&Reviews':RetRew,
        'Ratting':Ratting,
     
    }
    return render_template('results.html',result=product)
def gethtml(productName):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.google.com/',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('q', productName),
        ('otracker', 'search'),
        ('otracker1', 'search'),
        ('marketplace', 'FLIPKART'),
        ('as-show', 'on'),
        ('as', 'off'),
    )

    response = requests.get('https://www.flipkart.com/search',headers=headers, params=params)
    return response.text
@app.route('/submit',methods=['POST','GET'])
def submit():
        category=str(request.form['Category'])
        return redirect(url_for('hello', productName=category))

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    app.run(port=8080,debug=True)

from logging import debug
from types import MethodType
from flask import Flask, render_template, redirect,request,session,url_for,send_file
from numpy.core.fromnumeric import product
import requests
from bs4 import BeautifulSoup
import pandas as pd
from werkzeug.datastructures import Range


app = Flask(__name__,static_url_path='/static')
@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/scrap/<string:cate>/<int:pg>')
def scrap(cate,pg):
    name=[]
    ratting=[]
    mrp=[]
    nrat=[]
    price=[]
    off=[]
    for page in range(pg):
        u='https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}'.format(cate,page)
        res=requests.get(u)
        soup=BeautifulSoup(res.content,'html.parser')
        for i in soup.find_all('div',attrs={"class":"_3pLy-c row"}):
            nam=i.find('div',attrs={'class':"_4rR01T"})
            name.append(nam.text)
            if i.find('div',attrs={'class':"gUuXy-"}):
                rat=i.find('div',attrs={'class':"gUuXy-"})
                ratting.append(rat.text)
            else:
                ratting.append('0')
            if i.find('span',attrs={'class':'_1lRcqv'}):   
                rt=i.find('span',attrs={'class':'_1lRcqv'})
                nrat.append(rt.text)
            else:
                nrat.append('0')
            pric=i.find('div',attrs={'class':'_30jeq3 _1_WHN1'})
            mrp.append(pric.text)
            if i.find('div',attrs={"class":'_3I9_wc _27UcVY'}):
                ap=i.find('div',attrs={"class":'_3I9_wc _27UcVY'})
                price.append(ap.text)
            else:
                price.append('0')
            if i.find('div',attrs={'class':'_3Ay6Sb'}):
                offer=i.find('div',attrs={'class':'_3Ay6Sb'})
                off.append(offer.text)
            else:
                off.append('0')
            if len(name)<1:
                break
    if len(name)>1:     
        details={
            'Title':name,
            'Price':price,
            'MRP':mrp,
            'star Rating':nrat,
            'Off':off,
            'Rating& Reviews':ratting
            }
        df=pd.DataFrame(details)
        df.to_excel('scrap.xlsx')
    # return render_template('results.html',url=[details.to_html()])
        return render_template('results.html',tables=[df.to_html(classes='d')])

        
    name=[]
    brand=[]
    mrp=[]
    price=[]
    off=[]
    for page in range(pg):
        u='https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}'.format(cate,page)
        res=requests.get(u)
        soup=BeautifulSoup(res.content,'html.parser')
        for i in soup.find_all('div',attrs={'class':'_2B099V'}):
            if i.find('div',attrs={'class':'_2WkVRV'}):
                br=i.find('div',attrs={'class':'_2WkVRV'})
                brand.append(br.text)
            else:
                br=i.find('a',attrs={'class':"IRpwTa"})
                brand.append(br.text)
            tt=i.find('a',attrs={'class':"IRpwTa"})
            name.append(tt.text)
            pr=i.find('div',attrs={'class':'_30jeq3'})
            price.append(pr.text)
            if i.find('div',attrs={'class':'_3I9_wc'}):
                mr=i.find('div',attrs={'class':'_3I9_wc'})
                mrp.append(mr.text)
            else:
                mrp.append('0')
            if i.find('div',attrs={'class':'_3Ay6Sb'}):
                offer=i.find('div',attrs={'class':'_3Ay6Sb'})
                off.append(offer.text)
            else:
                off.append('0')
            if len(name)<1: 
                break
    if len(name)>1:
        details={
            'Brand':brand,
            'Title':name,
            'Price':price,
            'MRP':mrp,
            'Off':off,
            }  
        df=pd.DataFrame(details)
        df.to_excel('scrap2.xlsx')
        return render_template('results1.html',tables=[df.to_html(classes='d')])
    # return render_template('results.html',url=[details.to_html()])
       
        
    starrat=[]
    name=[]
    price=[]
    mrp=[]
    off=[]
    review=[]
    for page in range(pg):
        u='https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}'.format(cate,page)
        res=requests.get(u)
        soup=BeautifulSoup(res.content,'html.parser')
        for i in soup.find_all('div',attrs={'class':'_4ddWXP'}):
            tt=i.find('a',attrs={'class':'s1Q9rs'})
            name.append(tt.text)
            if i.find('div',attrs={'class':'_3LWZlK'}):
                rat=i.find('div',attrs={'class':'_3LWZlK'})
                starrat.append(rat.text)
            else:
                starrat.append('0')
            if i.find('span',attrs={'class':'_2_R_DZ'}):
                rew=i.find('span',attrs={'class':'_2_R_DZ'})
                review.append(rew.text)
            else:
                review.append('0')
            pr=i.find('div',attrs={"class":"_30jeq3"})
            price.append(pr.text)
            if i.find('div',attrs={'_3I9_wc'}):
                mr=i.find('div',attrs={'_3I9_wc'})
                mrp.append(mr.text)
            else:
                 mrp.append('0')
            if i.find('div',attrs={'class':'_3Ay6Sb'}):
                offer=i.find('div',attrs={'class':'_3Ay6Sb'})
                off.append(offer.text)
            else:
                 off.append('0')
            if len(name)<1:
                break
    if len(name)>1:         
        details={
            'Title':name,
            'Price':price,
            'MRP':mrp,
            'Ratting':starrat,
            'Off':off,
            'Review':review
            }       
        df=pd.DataFrame(details)
        df.to_excel('scrap3.xlsx')
        return render_template('results2.html',tables=[df.to_html(classes='d')])
    # return render_template('results.html',url=[details.to_html()])
        

       
@app.route('/download')
def download_file1():
    t="scrap.xlsx"
    return send_file(t,as_attachment=True)      
@app.route('/download')
def download_file2():
    q="scrap2.xlsx"
    return send_file(q,as_attachment=True)        
@app.route('/download')
def download_file3():
    q="scrap3.xlsx"
    return send_file(q,as_attachment=True)             
      
@app.route('/submit',methods=['GET','POST'])
def submit():
    Category=str( request.form['Category']) 
    page=int(request.form['Pages'])
    return redirect(url_for('scrap',cate=Category,pg=page))


# @app.route('/submit',methods=['POST','GET'])
# def submit():

#         category=str(request.form['Category'])
#         category='?'+category
#         return(redirect(url_for('products', productName=category)))

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    app.run(port=5000,debug=True)

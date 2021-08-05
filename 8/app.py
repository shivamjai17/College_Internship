from flask import Flask,redirect,render_template,request,url_for
import requests
from bs4 import BeautifulSoup
import pandas as pd

app =Flask(__name__,static_url_path='/static')

@app.route('/')
def show():
    return render_template('index.html')

@app.route('/hello/<int:pg>/<string:nam>')
def hello(pg,nam):
    starrat=[]
    name=[]
    price=[]
    mrp=[]
    off=[]
    review=[]
    for page in range(pg):
        u='https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}'.format(nam,page)
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
    details={
            'Title':name,
            'Price':price,
            'MRP':mrp,
            'star Rating':starrat,
            'Off':off,
            'Rating& Reviews':review
            }     
    df=pd.DataFrame(details)
    return render_template('results.html',tables=[df.to_html(classes='d')])
@app.route('/submit',methods=['POST','GET'])
def submit():

    total_score=0
    n=int(request.form['Page'])
    cate=str(request.form['Category'])
    return(redirect(url_for('hello',pg=n,nam=cate)))






if __name__ =='__main__':
    app.run(debug=True)
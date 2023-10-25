from flask import Flask,render_template,request,session, url_for, redirect,flash 
#from flask_mysqldb import MySQL
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#from sklearn import datasets
import pickle
import pymysql
import numpy as np
import math
import pickle
import collections
from sklearn.metrics import average_precision_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score,recall_score
from sklearn.metrics import roc_auc_score,roc_curve
from sklearn.metrics import auc
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import re
# from publicsuffixlist import PublicSuffixList
import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="creditcard")
    return connection

def dbClose():
    dbConnection().close()
    
    return

app=Flask(__name__)
app.secret_key = 'random string'
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/home.html')
def home():
    return render_template('home.html')


@app.route('/register',methods=['POST','GET'] )
def register():
    if request.method == "POST":
        try:
            status=""
            fname = request.form.get("name")
            add = request.form.get("add")
            pno = request.form.get("pno")
            email = request.form.get("email")
            pass1 =  request.form.get("pass1")
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userdetailes WHERE email = %s', (email))
            res = cursor.fetchone()
            #res = 0
            if not res:
                sql = "INSERT INTO userdetailes (name, address,phone,email,password) VALUES (%s,%s, %s, %s, %s)"
                val = (fname ,add ,pno ,email ,pass1)
                print(sql," ",val)
                cursor.execute(sql, val)
                con.commit()
                status= "success"
                return render_template("login.html")
            else:
                status = "Already available"
            #return status
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user',None)
        mailid = request.form.get("email")
        password = request.form.get("pass1")
        #print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetailes WHERE email = %s AND password = %s', (mailid, password))
        #a= 'SELECT * FROM userdetails WHERE mobile ='+mobno+'  AND password = '+ password
        print(result_count)
        #result_count=cursor.execute(a)
        # result = cursor.fetchone()
        if result_count>0:
            print(result_count)
            session['user'] = mailid
            return render_template("home.html")
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
    return render_template('login.html')


@app.route('/project.html')
def contact():
    return render_template('project.html')


@app.route('/credit',methods=['POST','GET'])
def credit():
    if request.method == "POST":
       # amt	zip	lat	long	merch_lat	merch_long	age
       import pandas as pd
       dff=pd.read_csv("preprocesscreditcard.csv")
       print(dff.columns)
       dict = {'amount':request.form.get("amount"),
                   'zip':request.form.get("zip"),
                   'lat':request.form.get("lat"),
                   'long':request.form.get("long"),
                   'merch_lat':request.form.get("merch_lat"),
                   'merch_long':request.form.get("merch_long"),
                   'age':request.form.get("age")}
       df=pd.DataFrame(dict,index=[0])
       print(df.columns)
       print(df)
    return render_template('credit.html')

if __name__=="__main__":
    app.run("0.0.0.0")
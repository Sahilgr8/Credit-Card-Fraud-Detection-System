from dataclasses import replace
from flask import *
import sqlite3,hashlib, os
from werkzeug.utils import secure_filename
# from flask import Flask, render_template, request
import pickle
import pymysql
import random,math
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import pandas as pd
global to_scale
from sklearn.feature_extraction.text import TfidfVectorizer
import socket
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#from date import   

app = Flask(__name__)

global prdt_name
global prdt_price
global productData1
#global totalPrice

# global loggedIn
# global firstName
# global noOfItems
global prdt_img
global total_amount
global outputofproposed
global newstatus
global user_id

def dbConnection():
    try:
        # connection = pymysql.connect(host="localhost", user="root", password="root", database="29polarity",charset='utf8')
        connection = pymysql.connect(host="localhost", user="root", password="root", database="hmmcredit",charset='utf8')
        return connection
    except:
        print("Something went wrong in database Connection")


def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        
def logindetails(): 
    con = dbConnection()
    cursor = con.cursor()
    uid = session['user_id']
    cursor.execute("SELECT count(productId) FROM kart WHERE userId = " + str(uid))
    noOfItems = cursor.fetchone()
    noOfItems = noOfItems[0]
    print(noOfItems)
    con.commit()
    #return(logedIn,firstname,noOfItems)
    return(noOfItems)



con=dbConnection()
cursor=con.cursor()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'random string'

##########################################################################################################
#                                           Register
##########################################################################################################
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        # print("hii register")
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        add = request.form['add']
        postc = request.form['postc']
        mob = request.form['mob']
        productId = 0
        print(password)
        print(email)
        print(username)
        print(add)
        print(mob)
        print(productId)
        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO users (username, email, pass) VALUES (%s, %s, %s)"
            val1 = (username, email, password)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            sql2 = "INSERT INTO address (username, email, address, postcode, mobile) VALUES (%s, %s, %s, %s, %s)"
            val2 = (username, email, add, postc, str(mob))
            cursor.execute(sql2, val2)
            print("query 2 submitted")
            # sql3 = "INSERT INTO kart1 (username, productId) VALUES (%s, %s)"
            # val3 = (username, int(productId))
            # cursor.execute(sql3, val3)
            # print("query 3 submitted")
            con.commit()
        except:
            con.rollback()
            msg = "Error occured"
            return render_template("login.html", error=msg)
        finally:
            dbClose()
        return render_template("login.html")
    return render_template("login.html")
##########################################################################################################
#                                               Login
##########################################################################################################
@app.route("/", methods = ['POST', 'GET'])
def login():
    global user_id
    if request.method == 'POST':
        global user_id
        email = request.form.get('email')
        password = request.form.get('password')

        # print(email)
        # print(password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM users WHERE email = %s AND pass = %s', (email, password))
        result = cursor.fetchone()
        print("result")
        
        print(result)
        if result_count>0:
            print("len of result")
            session['uname'] = result[1]
            session['user_id'] = result[0]
            session['usermail'] = email
            user_id = session['user_id']
            
            return redirect(url_for('root'))
        else:
            return render_template('login.html')
    return render_template('login.html')
##########################################################################################################
#                                       FORGOT PASSWORD
##########################################################################################################
@app.route("/forgot_pwd", methods=['POST', 'GET'])
def forgot_pwd():
    #username=session.get('uname')
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM users WHERE email = %s', (email))
        result = cursor.fetchone()
        if result_count>0:
            #print("user exist................")
            num = "0123456789"
            val = ""
            for i in range(0,6):
                val += num[math.floor(random.random()*10)]
            OTP = val + " is your One-Time-Password for verification"
            OTP1=val
            print(OTP1)
            #############################            
            con = dbConnection()
            print("db conection done")
            cursor = con.cursor()
            sql1 = ("UPDATE users SET otp = %s WHERE email = %s")
            val1 = (OTP1,email)
            result11=cursor.execute(sql1, val1)            
            print("query 1 submitted")
            con.commit()
            ############################            
            fromaddr = "donotreplycreditcard@gmail.com"
            toaddr = email          
            #instance of MIMEMultipart 
            msg = MIMEMultipart()           
            # storing the senders email address   
            msg['From'] = fromaddr           
            # storing the receivers email address  
            msg['To'] = toaddr          
            # storing the subject  
            msg['Subject'] = "Verify yourself!"          
            # string to store the body of the mail 
            body = "Your OTP is "+str(OTP1)+" Please verify otp  and take action for change the password.."
            # body = "Click on this link to verify yourself 'http://localhost:5000/validpage' and your OTP is"
         
            # attach the body with the msg instance 
            msg.attach(MIMEText(body, 'plain'))          
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587)          
            # start TLS for security 
            s.starttls()          
            # Authentication 
            s.login(fromaddr, "wzxkpaygyhdfmbsx") 
          
            # Converts the Multipart msg into a string 
            text = msg.as_string() 
          
            # sending the mail 
            s.sendmail(fromaddr, toaddr, text) 
          
            # terminating the session 
            s.quit() 
            # return redirect(url_for('login'))
            return "success" #script msg
        else:
            
            return "error" #Script Msg
        
    # return redirect(url_for('login'))
#########################################################################################################
#                                       CHANGE PASSWORD
#########################################################################################################
@app.route("/change_password", methods = ['POST', 'GET'])
def change_password():
    if request.method == 'POST':
        otp = request.form['otp']
        password = request.form['password']
        #print(otp)
        #print(password)
        con = dbConnection()
        cursor = con.cursor()
        email = session['email']
        print(email)
        result_count = cursor.execute('SELECT * FROM users WHERE otp=%s',(otp))
        result = cursor.fetchone()
        if result_count>0:
            sql = ('UPDATE users SET pass = %s WHERE email = %s ')
            val = (password,email)
            final_result = cursor.execute(sql,val)
            print("query submitted successfully...")
            con.commit()
            return "success"
        else:
            return "error"
            #print("error")
        session.pop('email', None)
    return render_template('login.html')
        
    
##########################################################################################################
#                                       Product Description
##########################################################################################################
@app.route("/single", methods = ['POST', 'GET'])
def productDescription():
    global prdt_name
    global prdt_price
    global productData1
    global loggedIn
    global firstName
    global noOfItems
    global prdt_img

    username=session.get('uname')
    productId = request.args.get('productId')
    
    print("######### productId ####")
    print(productId)
    con = dbConnection()
    cursor = con.cursor()

    cursor.execute('SELECT uname, comments FROM user_analysis where product_id = %s',(productId))
    cmnt = cursor.fetchall()
    print("### cmnt ####")
    print(cmnt)
    ################### fetching comments and username from database #############################
    unm=[]
    cm=[]
    for i in cmnt:
        a = i[0]
        unm.append(a)
        b = i[1]
        cm.append(b)
        # print("### a,b ####")
        # print(a,b)
        # break
    cmt = zip(unm,cm)  

    cursor.execute('SELECT name, price, description, image FROM product WHERE productId = ' + productId)
    productData = cursor.fetchone()
    productData = list(productData)
    # print("#### productData #####")
    # print(productData)

    prdt_name = productData[0]
    prdt_price = productData[1]
    prdt_disc = productData[2].split(',')
    productData1 = []
    for i in prdt_disc:
        prdt_disc1 = i.replace("\r\n","")
        productData1.append(prdt_disc1)
    print("#### prdt_disc #####")
    print(productData1)
    prdt_img = productData[3]


    cursor.execute('SELECT categoryId FROM product WHERE productId = ' + productId)
    cat_dat = cursor.fetchone()
    con.close()
    return render_template('single.html',cmt=cmt,  firstName=username, prdt_name=prdt_name, prdt_price=prdt_price,productId=productId, productData1=productData1, prdt_img=prdt_img )
##########################################################################################################
#                                               about
##########################################################################################################
@app.route("/about", methods = ['POST', 'GET'])
def about():
    username=session.get('uname')
    return render_template('about.html',firstName=username)
##########################################################################################################
#                                               Report
##########################################################################################################
@app.route("/report", methods = ['POST', 'GET'])
def report():
    username=session.get('uname')
    prd_name = request.args.get('prd_name')
    prd_name=list(prd_name.split('?'))
    prd_nm=prd_name[0]
    cmnt=prd_name[1]
    rprt=prd_name[2]

    # print("#### prd_name,cmnt,rprt ####")
    # print(prd_nm)
    # print(cmnt)
    # print(rprt)
    con = dbConnection()
    cursor = con.cursor()
    res_cont = cursor.execute('SELECT report FROM user_analysis WHERE product_name = %s and comments = %s', (prd_nm,cmnt))
    reprt = cursor.fetchone()
    # con.close()
    print("## reprt #")
    print(int(reprt[0]))
    report_num=int(reprt[0])
    report_num= report_num + 1

    sql1 = "UPDATE user_analysis SET report=%s WHERE product_name = %s and uname = %s"
    val1 = (str(report_num),prd_nm,username)
    cursor.execute(sql1, val1)
    con.commit()
    return redirect(url_for('root'))



    # return render_template('single.html',  firstName=username, prdt_name=prdt_name, prdt_price=prdt_price, productData1=productData1, prdt_img=prdt_img )
##########################################################################################################
#                                               contact
##########################################################################################################
@app.route("/contact", methods = ['POST', 'GET'])
def contact():
    username=session.get('uname')
    return render_template('contact.html',firstName=username)

##########################################################################################################
#                                               contact
##########################################################################################################
@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    # username=session.get('uname')
    session.pop('uname',None)
    return redirect(url_for('login'))
#######################################     ADD TO CART      #############################################
@app.route("/addTocart/<string:id>", methods = ['POST', 'GET'])
def addTocart(id):
    print("********************************************")
    if request.method == 'POST':
        quantity = request.form['quantity']
        #price = request.form['price']
        print(quantity)
       # noOfItems = logindetails()
       # print(noOfItems)
        print('hiiiiiiiiiiiiiiiiii')
        con = dbConnection()
        cursor = con.cursor()
        uid = session.get('user_id')
        uname = session.get('uname')
        sql = cursor.execute( "INSERT INTO kart (userId, username, productId, quantity) VALUES(%s,%s,%s,%s)", [uid,uname,id,quantity] )
        #print(sql)
        #total = 
        con.commit()
        return redirect(url_for('root'))
    #return render_template('index.html',noOfItems=noOfItems)
    
###################################     REMOVE FROM CART    ############################################
@app.route("/removefromCart/<string:id>", methods = ['POST', 'GET'])
def removefromCart(id):
    print("***************delete************************")
    pid = id
    uid = session.get('user_id')
    print(pid)
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM kart WHERE userId=%s AND productId=%s",[str(uid), str(pid)])
    con.commit()
    return redirect(url_for('root'))
    #return render_template('index.html')
    
#     return render_template('kart1.html',  firstName=username, categoryData=categoryData, product_lst_m=result11, product_lst_w=result2, product_lst_b=result3, product_lst_f=result4)


# @app.route("/addTocart", methods = ['POST', 'GET'])
# def addTocart():
#     print("********************************************")
#     if request.method == 'POST':
#         quantity = request.form.get('quantity')
#         product_Id = request.form.get('product_Id')
#         #price = request.form['price']
#         print(quantity)
#        # noOfItems = logindetails()
#        # print(noOfItems)
#         print('hiiiiiiiiiiiiiiiiii')
#         con = dbConnection()
#         cursor = con.cursor()
#         uid = session['user_id']
#         uname = session['uname']
#         sql = cursor.execute( "INSERT INTO kart (userId, username, productId, quantity) VALUES(%s,%s,%s,%s)", [uid,uname,product_Id,quantity] )
#         #print(sql)
#         #total = 
#         con.commit()
#         return redirect(url_for('root'))
#     #return render_template('index.html',noOfItems=noOfItems)
##########################################################################################################
#                                               Single page
##########################################################################################################
# @app.route("/kart", methods = ['POST', 'GET'])
# def kart():
#     global prdt_name
#     global prdt_price
#     global productData1
#     global loggedIn
#     global firstName
#     global noOfItems
#     global prdt_img

#     if request.method == 'POST':
#         productId = request.form['productId']
#         itm_name = request.form['item_name']
#         amnt = request.form['amount']
#         print("#### itm_name,amnt ########")
#         print(productId,itm_name,amnt)

#         username=session.get('uname')
#         print(username)

#         con = dbConnection()
#         cursor = con.cursor()
#         result_count = cursor.execute("SELECT name, price, description, image from product where name=%s", (itm_name))
#         result = cursor.fetchone()
#         result = list(result)
#         print(result)
#         print()

#         prd_name = result[0]
#         Price = result[1]
#         description = result[2]
#         img = result[3]

#         uname = session.get("uname")
#         result_count = cursor.execute("SELECT email, address, postcode, mobile from address where username=%s", (uname))
#         result2 = cursor.fetchone()
#         result2 = list(result2)
#         email = result2[0]
#         address = result2[1]
#         postcode = result2[2]
#         mobile = result2[3]

#         print()
#         print(result2)

#         sql1 = "INSERT INTO kart1 (username, email, address,postcode,mobile,prd_name,Price,description,img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         val1 = (uname, email, address,postcode,mobile,prd_name,Price,description,img)
#         cursor.execute(sql1, val1)
#         con.commit()
#         print("query submitted")

#         return render_template('kart.html',  firstName=username,description=description,Price=Price,prd_name=prd_name,img=img)
#     return render_template('single.html')

##########################################################################################################
#                                       Home page
##########################################################################################################
@app.route("/root")
def root():
    #global totalPrice
    if 'uname' in session:
        print(" hii root")
        username=session.get('uname')
        uid=session.get('user_id')
        print()
        print("printing user id")
        print(uid)
        print()
        con = dbConnection()
        cursor = con.cursor()
        ##########################    view products to user index root pg after login      ###########################################
        # MENS Products
        result_count=cursor.execute("SELECT * FROM product WHERE categoryId = 1")
        result11 = cursor.fetchall()
        print()
        print("result11")
        
        print()
        # WOMENS Products
        result_count1=cursor.execute("SELECT * FROM product WHERE categoryId = 2")
        result2 = cursor.fetchall()
        # bags Products
        result_count2=cursor.execute("SELECT * FROM product WHERE categoryId = 3")
        result3 = cursor.fetchall()
        # Footwear Products
        result_count3=cursor.execute("SELECT * FROM product WHERE categoryId = 4")
        result4 = cursor.fetchall()
        
        #####################################################################3
        # username = session.get("user")

        # cursor.execute("SELECT productId, name, price, description, image, stock FROM product")
        # result1 = cursor.fetchone()
        # cursor.execute("SELECT categoryId, name FROM categories")
        # categoryData = cursor.fetchone()
        cursor.execute("SELECT productId, name, price, description, image, stock FROM product")
        result1 = cursor.fetchone()
        cursor.execute("SELECT categoryId, name FROM categories")
        categoryData = cursor.fetchone()
        ################  CArt button modal index pg   #######
        uid = session.get('user_id')
        result = cursor.execute("SELECT product.productId,product.name,product.price,product.image,kart.quantity,(kart.quantity*product.price) as ProductPrice FROM product JOIN kart ON product.productid=kart.productid WHERE userId=" +str(uid))
        prod_val = cursor.fetchall()
        totalPrice = 0
        for row in prod_val:
            totalPrice += int(row[5])
        print(totalPrice)
        session['totalPrice'] = totalPrice
       # session['user_id'] = result[0]
        
        #################
        con.commit()   

    return render_template('index.html',totalPrice=totalPrice, firstName=username, categoryData=categoryData, product_lst_m=result11, product_lst_w=result2, product_lst_b=result3, product_lst_f=result4, prod_val=prod_val)

##########################################################################################################
#                                       Home page
##########################################################################################################
@app.route("/ordered", methods=["GET","POST"])
def ordered():
    if 'uname' in session and request.method=="POST":
        print(" hii root")
        username=session.get('uname')
        con = dbConnection()
        cursor = con.cursor()
        # username = session.get("user")

        # cursor.execute("SELECT productId, name, price, description, image, stock FROM product")
        # result1 = cursor.fetchone()
        # cursor.execute("SELECT categoryId, name FROM categories")
        # categoryData = cursor.fetchone()
        cursor.execute("SELECT productId, name, price, description, image, stock FROM product")
        result1 = cursor.fetchone()
        cursor.execute("SELECT categoryId, name FROM categories")
        categoryData = cursor.fetchone()
        con.commit()   

        flash("Your order has been placed! Thank you for shopping!","order")

    return render_template('index.html',  firstName=username, categoryData=categoryData)

##########################################################################################################
#                                      Admin part
##########################################################################################################
@app.route("/adregister", methods = ['GET', 'POST'])
def adregister():
    if request.method == 'POST':
        #Parse form data    
        # print("hii register")
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        print(password)
        print(email)
        print(username)
        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO admin (username, email, pass) VALUES (%s, %s, %s)"
            val1 = (username, email, password)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            con.commit()
        except:
            con.rollback()
            msg = "Error occured"
            return render_template("admin.html", error=msg)
        finally:
            dbClose()
        return render_template("admin.html")
    return render_template("admin.html")

@app.route("/adlogin", methods = ['POST', 'GET'])
def adlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 

        # print(email)
        # print(password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM admin WHERE email = %s AND pass = %s', (email, password))
        result = cursor.fetchone()
        print("result")
        print(result)
        if result_count>0:
            print("len of result")
            session['uname'] = result[1]
            session['userid'] = result[0]
            return redirect(url_for('adhome'))
        else:
            return render_template('admin.html')
    return render_template('admin.html')

@app.route("/adhome")
def adhome():
    if 'uname' in session:
        global final_data
        print(" hii root")
        username=session.get('uname')
        con = dbConnection()
        cursor = con.cursor()
        ##########################    view products to admin home      ###########################################
        # MENS Products
        result_count=cursor.execute("SELECT * FROM product WHERE categoryId = 1")
        result1 = cursor.fetchall()
        # WOMENS Products
        result_count1=cursor.execute("SELECT * FROM product WHERE categoryId = 2")
        result2 = cursor.fetchall()
        # bags Products
        result_count2=cursor.execute("SELECT * FROM product WHERE categoryId = 3")
        result3 = cursor.fetchall()
        # Footwear Products
        result_count3=cursor.execute("SELECT * FROM product WHERE categoryId = 4")
        result4 = cursor.fetchall()
        return render_template('adhome.html',product_lst_m=result1, product_lst_w=result2,product_lst_b=result3,product_lst_f=result4)
        
        
        # result_count1=cursor.execute("SELECT * FROM product WHERE categoryId = 2")
        # result2 = cursor.fetchall()
        
        # if result_count1>0:
        #     return render_template('adhome.html', product_lst_w=result2)
        
        
        
        ##########################################################################################################
        cursor.execute("SELECT * FROM user_analysis")
        result1 = cursor.fetchall()
        print("### result1 ###")
        print(result1)
        con.commit()   
        user_data = list(result1)

        sr_no=[]
        prdct_id=[]
        prdct_name=[]
        uname=[]
        cmnts=[]
        ipad=[]
        real_fk=[]
        tim_stmp=[]
        by_not=[]
        rprt_count=[]
        for i in user_data:
            a=i[0]
            print("### printing a ###")
            print(a)
            sr_no.append(a)

            b=i[1]
            prdct_id.append(b)

            c=i[2]
            prdct_name.append(c)

            d=i[3]
            uname.append(d)

            e=i[4]
            cmnts.append(e)

            f=i[5]
            ipad.append(f)

            g=i[6]
            real_fk.append(g)

            h=i[7]
            tim_stmp.append(h)

            l=i[8]
            by_not.append(l)

            j=i[9]
            rprt_count.append(j)
        
        final_data=zip(sr_no,prdct_id,prdct_name,uname,cmnts,ipad,real_fk,tim_stmp,by_not,rprt_count)
        return render_template('adhome.html',  firstName=username, final_data=final_data)
    return render_template('adhome.html')
###########################################      ADD PRODUCT         ####################################################

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if request.method == "POST":
        pname = request.form['pname']
        price = request.form['price']
        description = request.form['desc']
        image = request.files['file']
        stock = request.form['stock']
        category = request.form['category']
        offer = request.form['offer']
        print(pname)
        filename_secure = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename_secure))
        filenamepath = os.path.join(app.config['UPLOAD_FOLDER'],filename_secure)
        ff = filename_secure
        # try:            
        con = dbConnection()
        print("Connection done.......................")
        cursor = con.cursor()
        sql = "INSERT INTO product (name,price,description,image,stock,categoryId,offers) VALUES(%s,%s,%s,%s,%s,%s,%s) "
        print(sql)
        val =(pname,price,description,ff,stock,category,offer)
        cursor.execute(sql,val)        
        print("query submitted.........")
        con.commit()
        msg = "Product Added Successfully................."
        return render_template("addproduct.html", msg=msg)
                
    return render_template('addproduct.html')

###########################################     Graph PRODUCT REPORT      ####################################################
from random import shuffle
@app.route('/productreport', methods=['POST', 'GET'])
def productreport():
    con = dbConnection()
    cur1 = con.cursor()
    res_count1 = cur1.execute("SELECT nofraud_status from fraud")
    res1 = cur1.fetchall()
    
    con = dbConnection()
    cur2 = con.cursor()
    res_count2 = cur2.execute("SELECT nofraud_status from nofraud")
    res2 = cur2.fetchall()

    chart_lst = []
    # flist = zip(result1,result2)
    if res_count1 > 0:
        
        result1 = list(res1)
        print(result1)
        for i in result1:
            if i[0] == "FraudDetected":
                a = 1
                chart_lst.append(a)
    if res_count2 > 0:
        result2 = list(res2)
        print(result2)
        for j in result2:
            if j[0] == "NoFraudDetected":
                a = 0
                chart_lst.append(a)
    shuffle(chart_lst)
    print(chart_lst)
    return render_template("productstock.html",  chart_lst=chart_lst)           
###################################################################################################################
dff = pd.read_csv("label_process.csv")
res = {}
job = dff["job"].unique()
job_lbl = dff["job_lbl"].unique()

flst = zip(job,job_lbl)
for key, val in flst:
    res[key] = val
    
@app.route('/checkout', methods=['POST', 'GET'])
def checkout():

    category=dff["category"].unique()
    category_lbl=dff["category_lbl"].unique()
    final_category = zip(category,category_lbl)
    
    gender=dff["gender"].unique()
    gender_lbl=dff["gender_lbl"].unique()
    final_gender=zip(gender,gender_lbl)
    
    city=dff["city"].unique()
    city_lbl=dff["city_lbl"].unique()
    final_city=zip(city,city_lbl)
    
    state=dff["state"].unique()
    state_lbl=dff["state_lbl"].unique()
    final_state=zip(state,state_lbl)
    
    totalPrice1 = session['totalPrice']
    
    return render_template("payment.html",final_gender=final_gender,totalPrice1=totalPrice1,final_category=final_category,final_city=final_city,final_state=final_state)
###########################################      Payment REPORT      ####################################################
from scipy.spatial import distance
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 

def proposedlogic(finaldff):
    df1=pd.read_csv('wrongoutput.csv',sep=',',error_bad_lines=False)
    df=df1#.sample(n=1000,replace=True)
    X = df.iloc[:,:-1].values # We drop our "target" feature and use all the remaining features in our dataframe to train the model.
    y = df.iloc[:,-1].values

    X = df[['amt', 'lat', 'long', 'category_lbl', 'gender_lbl', 'city_lbl','state_lbl', 'job_lbl']] # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
    Y = df['is_fraud']
    X1 = X.iloc[:,:].values # We drop our "target" feature and use all the remaining features in our dataframe to train the model.
    finaldff = finaldff.apply(pd.to_numeric, errors='coerce')
    
    print("----------printing finaldff -------------")
    print(finaldff)
    print()
    
    X2=finaldff.iloc[:,:].values
    
    outexpect=[]
    overall=[]
    for row in X2:
        countis=0
        for row1 in X1:
            y=row
            summation = 0
            y_bar=row1
            n = len(y) #finding total number of items in list
            for i in range (0,n):  #looping through each element of the list
                print("----------printing finaldff -------------")
                print(finaldff)
                print(y[i])
                print(y_bar[i])
                print()
                difference = float(y[i]) - float(y_bar[i])  #finding the difference between observed and predicted value
                squared_difference = difference**2  #taking square of the differene 
                summation = summation + squared_difference  #taking a sum of all the differences
            MSE = summation/n  #dividing summation by total values to obtain average
            print("The Mean Square Error is: " , MSE)
            dst = distance.euclidean(y, y_bar)
            print("dst is: " , dst)
            if dst>1000:
                outexpect.append(1.0)
            else:
                outexpect.append(0.0)
            if MSE>=100000:
                outexpect.append(1.0)
            else:
                outexpect.append(0.0)
            if len(outexpect)>10:
                break
    if outexpect[-1]==1.0:
        final_output = 1.0
        overall.append(final_output)
    else:
        final_output = 0.0
        overall.append(final_output)
    return overall


def sendemailtouser(sendto,value):    
    fromaddr = "psystem0801@gmail.com"
    toaddr = sendto
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Verify yourself!"
  
    # string to store the body of the mail 
    body = "Your OTP is "+str(value)+" Please verify otp on 'http://localhost:5000/checkotp' this link and take action for credit card transaction"
    # body = "Click on this link to verify yourself 'http://localhost:5000/validpage' and your OTP is"

  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "kgjdmlgfdhbmtmke") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit()    



from sklearn.preprocessing import LabelEncoder

mydata3 = pd.read_csv('fraudTrain.csv')

le1 = LabelEncoder()
le1.fit(mydata3["category"])
le2 = LabelEncoder()
le2.fit(mydata3["gender"])
le3 = LabelEncoder()
le3.fit(mydata3["city"])
le4 = LabelEncoder()
le4.fit(mydata3["state"])
le5 = LabelEncoder()
le5.fit(mydata3["job"])


filename='hmm_module.sav'
loaded_model_nb = pickle.load(open(filename, 'rb'))

from random import randint
import random
from geopy.geocoders import Nominatim
import geocoder

@app.route('/payment', methods=['POST', 'GET'])
def payment():
    global total_amount
    global outputofproposed
    global newstatus
    uid = session.get('user_id')
    Current_Date = datetime.date.today()
    print ('Current Date: ' + str(Current_Date))  
    totalPrice1 = session['totalPrice']
    print("totalPrice1="+ str(totalPrice1))
    print("************************")
    
    if request.method == "POST":
        # validate = list(request.form.values())
        card_name = request.form.get("name")
        total_amount = request.form.get("amount").replace("$","")
        category_inp = request.form.get("category")
        gender_inp = request.form.get("gender")
        city_inp = request.form.get("city")
        state_inp = request.form.get("state")

        job_lst = list(mydata3["job"].unique())
        random_job = random.choice(job_lst)
        Trandom_job = res[random_job]
        # print("random_job")
        # print(random_job)
        # print(le5.transform([random_job]))
        # print(le5.transform([random_job])[0])

        print("validate")
        print(card_name,total_amount,category_inp,gender_inp,city_inp,state_inp)
        
        gender_dict = {"F":0,"M":1}

        # initialize Nominatim API
        geolocator = Nominatim(user_agent="geoapiExercises")

        g = geocoder.ip('me')
        print(g.latlng)

        # Latitude & Longitude input
        Latitude = g.latlng[0]
        Longitude = g.latlng[1]
        
        # newlst=[totalPrice1,float(Latitude),float(Longitude),le1.transform([validate[2]])[0],le2.transform([validate[3]])[0],le3.transform([validate[4]])[0],le4.transform([validate[5]])[0],float(le5.transform(["Transport planner"]))]
        # newlst=[float(le2.transform(category_inp)[0]),float(total_amount),float(gender_dict[gender_inp]),le3.transform([city_inp])[0],le4.transform([state_inp])[0], le3.transform([Latitude])[0], le4.transform([Longitude])[0],le5.transform([Trandom_job])[0]]
        newlst=[float(total_amount),float(Latitude),float(Longitude),float(category_inp),float(gender_inp),int(city_inp),int(state_inp),int(Trandom_job)]
        # newlst=[totalPrice1,float(validate[6]),float(validate[7])]
        print("newlist:")
        print(newlst)
        data = pd.DataFrame(newlst).T
        
        print("data:-")
        print(data)
        data.columns = ['amt','lat','long','category_lbl','gender_lbl','city_lbl','state_lbl','job_lbl']
        
        nb=loaded_model_nb.predict(pd.DataFrame(data)) 
        
        finaldff = pd.DataFrame(data)           
        outputofproposed=proposedlogic(finaldff)
        print("----------------")
        print(nb)
        print(outputofproposed)
        print("----------------")
        output=nb[0]
        # output = 0
        if output==0:
            msg="NoFraudDetected"
            con = dbConnection()
            cursor = con.cursor()
            sql = "INSERT INTO nofraud (userid,category,amount,gender,city,state,latitude,longitude,nofraud_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (str(uid),str(request.form.get("category")),str(totalPrice1),str(request.form.get("gender")),str(request.form.get("city")),str(request.form.get("state")),str(Latitude),str(Longitude),msg)
            print(sql," ",val)
            cursor.execute(sql, val)
            con.commit()
            if outputofproposed[0] == 0.0: 
                print("If")
                flash("According to HMM : No Fraud Detected")
                # flash("According to Euclidean : No Fraud Detected")
                return redirect(url_for('payment'))
            else:  
                print("Else")                  
                flash("According to HMM : No Fraud Detected")
                # flash("According to Euclidean : Fraud Detected")
                return redirect(url_for('payment'))
                
        else:
           print("__________________________we are in Else _____________________________________")
           print(session.get('user_id'))
           msg="FraudDetected"
           value = randint(100000, 600000)
           con = dbConnection()
           cursor = con.cursor()
           sql = "INSERT INTO fraud (userid,category,amount,gender,city,state,latitude,longitude,job,nofraud_status,otp_gen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
           val = (str(uid),str(request.form.get("category")),str(totalPrice1),str(request.form.get("gender")),str(request.form.get("city")),str(request.form.get("state")),str(Latitude),str(Longitude),str(Trandom_job),str(msg),str(value))
           print(sql," ",val)
           cursor.execute(sql, val)
           con.commit()
           newstatus = msg
           usermail=session.get('usermail')
           print(usermail)     
           sendemailtouser(usermail,value)
           msg="Please check your mail and verify yourself! OTP is sent on mail"
           flash(msg)                
           if outputofproposed[0] == 0.0: 
               print("If")                   
               flash("According to HMM : Fraud Detected")
            #    flash("According to Euclidean : No Fraud Detected")
               flash(msg)
               return redirect(url_for('payment'))
           else:        
               print("Else")                    
               flash("According to HMM : Fraud Detected")
            #    flash("According to Euclidean : Fraud Detected")
               flash(msg)           
               return redirect(url_for('payment'))
    
    
    return render_template('razor_payment.html',total_amount=total_amount, public_key=public_key)

     
    
    
    # if request.method == 'POST':
    #     number = request.form['number']
    #     name = request.form['name']
    #     #totalAmount = request.form['amount']
    #     exp = request.form['exp']
    #     print("Card Number=" +number+"my name")
    #     print("Cardholder's Name=" +name)
    #     #print(totalAmount)         
    #     print("expiryDate=" +exp)
        #######################################
       
        
        # con = dbConnection()
        # cursor = con.cursor()
       
        # cursor.execute("SELECT kart.username, kart.quantity,product.categoryId,product.productId FROM kart JOIN product ON product.productId=kart.productId WHERE userId= "+str(uid))
        # kartProduct = cursor.fetchall()    
        
        # for i in kartProduct:
        #     Quantity = i[1]
        #     categoryId = i[2] 
        #     productId = i[3]  
        #     query1 = "INSERT INTO user_prod_details(userId,date,category,quantity) VALUES (%s,%s,%s,%s)"
        #     val = (uid,Current_Date,categoryId,Quantity)          
        #     print(val)     
  
        #     cursor.execute(query1,val)          
        #     print("query submitted.........")
        #     con.commit()
        #     query2 = "UPDATE product SET stock = stock - %s Where productId=%s"
        #     val2   = (Quantity,productId)
        #     cursor.execute(query2,val2) 
        #     con.commit()
           
        # cursor.execute("DELETE FROM kart WHERE userId=%s",[str(uid)])       
        # con.commit()
        # msg = "Pyament Sccessfull!......."
        # return redirect(url_for('root'))
        # session.pop('totalPrice',None)
        # print("totalPrice="+totalPrice)
    return render_template('index.html')

import stripe

public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

@app.route('/thankyou')
def thankyou():
    global outputofproposed
    final_op = outputofproposed
    
    # final_msg1 = "Please check your mail and verify yourself! OTP is sent on mail"
    # final_msg2 = "Congratulations your order has been placed successfully!"
    final_msg1 = "Please check your mail and verify yourself! OTP is sent on mail"
    final_msg2 = "Congratulations your order has been placed successfully!"
    if final_op[0] == 0.0:          
        msg1 = "According to HMM : Fraud Not Detected"
        # msg2 = "According to Euclidean : No Fraud Detected"
        final_msg = final_msg2
        user_session_id = session.get("userid")
        
        conn = dbConnection()
        curs = conn.cursor()
        curs.execute("delete from kart where userId=%s ORDER BY userId DESC LIMIT 1;",(str(user_session_id)))
        conn.commit()
        # select *from getLastRecord ORDER BY id DESC LIMIT 1;
        return render_template('thankyou.html',final_msg=final_msg,msg1=msg1)
    else:                
        msg1 = "According to HMM : Fraud Detected"
        # msg2 = "According to Euclidean : Fraud Detected"
        final_msg = final_msg1
        return render_template('thankyou.html',final_msg=final_msg,msg1=msg1)

@app.route('/payment2', methods=['POST'])
def payment2():
    global total_amount
    # CUSTOMER INFO
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # PAYMENT INFO
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=total_amount, # 19.99
        currency='USD',
        description='Donation'
    )
    
    user_id = session.get("userid")

    return redirect(url_for('thankyou'))

@app.route('/resendotp', methods=['POST','GET'])
def resendotp():
    global newstatus
    global total_amount
    global user_id
    
    umail = session.get("usermail")
    Uid = user_id
    amnt = total_amount
    
    conn = dbConnection()
    curs = conn.cursor()
    sql = "SELECT otp_gen from fraud where userid=%s and amount=%s ORDER BY id DESC LIMIT 1;"
    val = (Uid,amnt)
    print(sql,val)
    result_count = curs.execute(sql,val)
    res = curs.fetchone()
    print()
    print("res in fraud \n:",res)
    print("result_count \n ",result_count)
    dbot  = res[0]

    sendemailtouser(umail,dbot)

    return "Please find otp in your mail"


@app.route("/checkotp",methods=['POST','GET'])
def checkotp():
    global newstatus
    global total_amount
    global user_id
    if request.method=="POST":
        global newstatus
        global total_amount
        global user_id


        # print(newstatus)
        # print(user_id)
        otptxt = request.form.get("otptxt")
        Uid = user_id
        amnt = total_amount
        
        print("printing otp")
        print(otptxt)

        # Uid = 2
        # amnt = 890
        print()
        print("priting global amount")
        print(Uid,amnt)
        print()        
        conn = dbConnection()
        curs = conn.cursor()
        sql = "SELECT otp_gen from fraud where userid=%s and amount=%s ORDER BY id DESC LIMIT 1;"
        val = (Uid,amnt)
        print(sql,val)
        result_count = curs.execute(sql,val)
        res = curs.fetchone()
        print()
        print("res in fraud \n:",res)
        print("result_count \n ",result_count)
        dbot  = res[0]
        print(dbot)
        if str(dbot)==str(otptxt):
            
            user_session_id = session.get("userid")
            conn = dbConnection()
            curs = conn.cursor()
            sql = "delete from kart where userId=%s ORDER BY userId DESC LIMIT 1;"
            val = (Uid)
            curs.execute(sql,val)
            conn.commit()
            return render_template("validationpage.html")
        else:
            msg = "Your OTP is invalid!"
            return msg
    return render_template("checkotp.html")

           
###################################################################################################################
@app.route("/analysis")
def analysis():
    if 'uname' in session:
        print(" hii root")
        username=session.get('uname')
        con = dbConnection()
        cur = con.cursor()
        cur.execute("select * from user_analysis")
        result = cur.fetchall()
        result = list(result)
        product_id = []
        product_name = []
        uname = []
        comments = []
        ipadd = []
        nb_real_fake = []
        svm_real_fake = []
        rf_real_fake = []
        time_stmp = []
        buy1_not0 = []
        report = []

        for i in result:
            a = i[1]
            product_id.append(a)
            b = i[2]
            product_name.append(b)
            c = i[3]
            uname.append(c)
            d = i[4]
            comments.append(d)
            e = i[5]
            ipadd.append(e)
            f = i[6]
            nb_real_fake.append(f)
            g = i[7]
            svm_real_fake.append(g)
            h = i[8]
            rf_real_fake.append(h)
            j = i[9]
            time_stmp.append(j)
            k = i[10]
            buy1_not0.append(k)
            l = i[11]
            report.append(l)

        flst = zip(product_id,product_name,uname,comments,ipadd,nb_real_fake,svm_real_fake,rf_real_fake,time_stmp,buy1_not0,report)

        final_score=[]
        for product_id,product_name,uname,comments,ipadd,nb_real_fake,svm_real_fake,rf_real_fake,time_stmp,buy1_not0,report in flst:
            umarks = []
            print()
            print(product_id,product_name,uname,comments,ipadd,nb_real_fake,svm_real_fake,rf_real_fake,time_stmp,buy1_not0,report)
            print()

            # Algorithms to identify fake and correct will used
            if nb_real_fake == "Negative" and svm_real_fake == "Negative" and rf_real_fake == "Negative":
                a = 20+20+20
                umarks.append(a)
            elif nb_real_fake == "Positive" and svm_real_fake == "Negative" and rf_real_fake == "Negative":
                a = 0+20+20
                umarks.append(a)
            elif nb_real_fake == "Negative" and svm_real_fake == "Positive" and rf_real_fake == "Negative":
                a = 20+0+20
                umarks.append(a)
            elif nb_real_fake == "Negative" and svm_real_fake == "Negative" and rf_real_fake == "Positive":
                a = 20+20+0
                umarks.append(a)
            else:
                a = 0+0+0
                umarks.append(a)

            cur.execute("select uname,time_stmp,comments from user_analysis where ipadd=%s",(ipadd))
            unameres = cur.fetchall()
            unameres = list(unameres)

            if len(comments)>0 and len(unameres)>1 and buy1_not0 == "0" and report=="1":
                b = 10+10+10+10
                umarks.append(b)
            elif len(comments)>0 and len(unameres)>1 and buy1_not0 == "1" and report=="0":
                b = 10+10+0
                umarks.append(b)
            else:
                b = 0+0+0
                umarks.append(b)

            final_score.append(umarks)
            print()
            print("printing umarks list: ",umarks)
            print()
            print("printing sum of umarks: ",sum(umarks))
            print()
            sum_score = sum(umarks)
            
            ftag = ""
            if sum_score>=70:
                ftag+="Positive"
            else:
                ftag+="Negative"

            sql = "INSERT INTO final_score(product_id,product_name,uname,comments,ipadd,nb_real_fake,svm_real_fake,rf_real_fake,time_stmp,buy1_not0,report,final_sum,final_tag) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (product_id,product_name,uname,comments,ipadd,nb_real_fake,svm_real_fake,rf_real_fake,time_stmp,buy1_not0,report,sum_score,ftag)
            cur.execute(sql,val)
            con.commit()
        
        con = dbConnection()
        cur = con.cursor()
        cur.execute("select * from final_score")
        result = cur.fetchall()
        result = list(result)
        product_id = []
        product_name = []
        uname = []
        comments = []
        ipadd = []
        nb_real_fake = []
        svm_real_fake = []
        rf_real_fake = []
        time_stmp = []
        buy1_not0 = []
        report = []
        score_sum = []
        final_tag = []
        uid = []

        for i in result:
            x = i[0]
            uid.append(x)
            a = i[1]
            product_id.append(a)
            b = i[2]
            product_name.append(b)
            c = i[3]
            uname.append(c)
            d = i[4]
            comments.append(d)
            e = i[5]
            ipadd.append(e)
            f = i[6]
            nb_real_fake.append(f)
            g = i[7]
            svm_real_fake.append(g)
            h = i[8]
            rf_real_fake.append(h)
            j = i[9]
            time_stmp.append(j)
            k = i[10]
            buy1_not0.append(k)
            l = i[11]
            report.append(l)
            m = i[12]
            score_sum.append(m)
            n = i[13]
            final_tag.append(n)

        flst1 = zip(uid,product_id,product_name,uname,comments,ipadd,nb_real_fake,svm_real_fake,rf_real_fake,time_stmp,buy1_not0,report,score_sum,final_tag)

        return render_template('analysis2.html',  firstName=username,flst1=flst1)
    return render_template('login.html')


if __name__=='__main__':
    # app.run(debug=True)
    app.run('0.0.0.0')
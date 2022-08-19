# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 18:19:45 2022

@author: Admin
"""
from cryptography.fernet import Fernet
from markupsafe import Markup
from flask import *
from flask_session import Session

key = Fernet.generate_key()
fernet = Fernet(key)


class Person:
    username = ''
    password = ''


def hashed(s):
    return s
    return fernet.encrypt(s.encode())
def dehash(s):
    return s
    return fernet.decrypt(s).decode()


import mysql.connector as mysql

conn = mysql.connect(host = "localhost", username = "root" , passwd = "Pettaashu2003")
cur = conn.cursor()

def use_database():
    query = "use linktree;"
    cur.execute(query)
    conn.commit()
    
def create_database_tables():
    
    try:
        query = "create database linktree;"
        cur.execute(query)
        conn.commit()
        use_database();
        
        query = "create table user_details(username varchar(15) primary key, password varchar(255) );"
        cur.execute(query)
        conn.commit()
        query = "create table linktree_details(username varchar(15) , field varchar(255)  , link varchar(255) );"
        cur.execute(query)
        conn.commit()
        
        print("queries executed successfully , all set !")
    except:
        pass

        
create_database_tables()
use_database()


app = Flask(__name__)
app.secret_key = "abc"  

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

login_user = ""

@app.route("/home.html" , methods = ["GET" , "POST"])
def home_page():
    return render_template("home.html")
    

@app.route("/create.html" , methods = ["GET" , "POST"])
def create_linktree():
    
    if not session.get("name"):
        flash("Please login to continue")
        return redirect("login.html")
    
    if request.method == "POST":
        
        field= request.form.get("field")
        link = request.form.get("link")
        
        
        if ((field.strip() != "") and (link.strip() != "")):
            
            query="insert into linktree_details values('{}' , '{}' , '{}' );".format(session["name"] , field , link)
            cur.execute(query)
            conn.commit()
            
    msg = '<table border = "10">'
    msg += '<tr><td>FIELD</td><td>LINK</td></tr>'
    query = "select field , link  from linktree_details where username like '{}'".format(session["name"])
    cur.execute(query)
    for i in cur.fetchall():
        msg += "<tr><td>"+i[0]+"</td> <td>" +i[1]+"</td></tr>" 
    msg += "</table>"
    return render_template("create.html" , msg = Markup(msg))

@app.route("/view.html" , methods = ["GET","POST"])
def view():
    
   if not session.get("name"):
       flash("YOU MUST LOGIN !")
       return redirect("login.html")
   else:
       name = session["name"]
       return redirect("view_.html?name="+name)

@app.route("/view_.html" , methods = ["GET","POST"])
def with_parameters():
    name = request.args.get("name")
    msg = '<center><h2>'+name+'</h2>'
    query = "select field , link  from linktree_details where username like '{}'".format(name)
    cur.execute(query)
    for i in cur.fetchall():
        msg += "<br><br><br><button id = 'click' onclick = \" window.location.href = '"+i[1]+"'\"; >"+i[0].upper()+"</button>" 
    msg += "</center>"
    return render_template("view.html" , msg = Markup(msg))

@app.route("/login.html" , methods = ["GET" , "POST"])
def login():
    
    if session.get("name"):
        flash("Please logout to login as new user !")
        return redirect("home.html")
    
    if request.method == "POST":
        #logged in
        #check database
        username = request.form.get("username")
        password = request.form.get("password")
        
        query = "select password from user_details where username = '"+username+"';"
        
        cur.execute(query)
        l =  cur.fetchall()
        print(l)
        
        try:
            passwd = l[0][0]
            print(passwd , password , passwd == password)
            if passwd == password:
                flash("logged in")
                session["name"] = username
            else:
                flash("WRONG PASSWORD ")
        except:
            flash("NO USER EXIST")
            
    
    return render_template("login.html")


def create_record(new_user , table_name):
    
    username = new_user.username
    password = hashed(new_user.password)
    
    query = "insert into "+table_name+' values("{}" , "{}" );'.format(username , password)
    print(query)
    
    try:
        cur.execute(query)
        conn.commit()
        return "insertion done"
    except:
        return "error"
    
@app.route("/signup.html" , methods = ["GET" , "POST"])
def signup():
    
    
    if session.get("name"):
        flash("You cannot SIGN UP !")
        return redirect("home.html")
    msg = ''
    if request.method == "POST":
        
        new_user = Person()
        new_user.username = request.form.get('username')
        new_user.password = request.form.get('password')
        
        response = create_record(new_user , "user_details")
        
        if response == "insertion done":
            flash("Your account is created ")
            return render_template("signup.html")
        else:
            flash("Username already exist!")
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route("/logout.html" , methods = ["GET" , "POST"])
def logout():
    if session.get("name"):
        session.pop("name" , None)
        flash("LOG OUT SUCCESSFULL !")
        return redirect("home.html")
    else:
        flash("You must Login in order to log out")
        return redirect("login.html")
    

app.run()
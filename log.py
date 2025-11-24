from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib
import dlib
import numpy as np
import cv2
import os
import shutil
import time
import logging
import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import sqlite3
import datetime
import pandas as pd
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import otp_sender
################################
import get_faces_from_camera_tkinter
import attendance_taker
import features_extraction_to_csv
from datetime import datetime
################################
import smtplib
from Cryptodome.Random import get_random_bytes,random
from base64 import b64encode
####################################

app = Flask(__name__)
app.secret_key = "key"

# Enter your database connection details below
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Humam.HR10"
app.config["MYSQL_DB"] = "LOGIN"

# Initialize MySQL
mysql = MySQL(app)
current_time = datetime.now()

    
def check_password_complexity(password):
    # Check if password meets complexity requirements
    if not (
        len(password) >= 10
        and any(p in punctuation for p in password)
        and any(p in ascii_lowercase for p in password)
        and any(p in ascii_uppercase for p in password)
        and any(p in digits for p in password)
    ):
        return False
    return True
username=""

@app.route("/", methods=["GET", "POST"])
def login():
    # Output message if something goes wrong...
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        global username
        username = request.form["username"]
        password = request.form["password"]
        password = password.encode("utf-8")
        sha512_hash = hashlib.sha512()
        sha512_hash.update(password)
        password = sha512_hash.hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM form WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        # Fetch one record and return result
        account = cursor.fetchone()
        
        
         
        
        if account:
            
            attendance = attendance_taker.Face_Recognizer()
            attendance.run()
            
            if attendance.name==username :
                
            # Create session data, we can access this data in other routes
                session["loggedin"] = True
          # session["id"] = account["id"]
                session["username"] = account["username"]
                
            # Redirect to home page
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                "SELECT email FROM form WHERE username = %s",
                (
                   username,
                ),
            )  
                
                email = cursor.fetchone()
                email=email['email']
            
            
            
                otp_code = otp_sender.otp_send(email)
                return render_template("otp_login.html",otp_code=otp_code)
                #return redirect(url_for("home"))
        else:
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT email FROM form WHERE username = %s",
                (
                   username,
                ),
            )
            email = cursor.fetchone()
            cursor.execute(
                "INSERT INTO general_logs (action, time_of_action, username, password, email) VALUES (%s, %s, %s, %s, %s)",
                (
                    "Unsuccessful Login",
                    current_time,
                    username,
                    password,
                    email,
                ),
            )
            mysql.connection.commit()

            # Account doesn't exist or username/password incorrect
            msg = "Incorrect username/password!"
            
    return render_template("index.html", msg=msg)


@app.route("/home", methods=["GET", "POST"])
def home():

    if "loggedin" in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM form WHERE username = %s",
                (
                   username,
                ),
               )
            line = cursor.fetchone()
            username_ = line['username']
            password = line['password']
            email = line['email']
            cursor.execute(
                "INSERT INTO general_logs (action, time_of_action, username, password, email) VALUES (%s, %s, %s, %s, %s)",
                (
                    "Successful Login",
                    current_time,
                    username,
                    password,
                    email,
                ),
            )
            mysql.connection.commit()
    
    
        
            return render_template(
                "mainpage.html", username=session["username"], hint=session.get("hint")
            )
    else:
            return redirect(url_for("login"))

    # User is not logged in, redirect to login page
    return redirect(url_for("login"))



@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    # Redirect to login page
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    # Output message if something goes wrong...
    msg = ""
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM form WHERE email = %s", (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = "Account already exists!"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
        elif not check_password_complexity(password):
            msg = "Password must contain at least 1 number, 1 lowercase letter, 1 uppercase letter, and 1 special character, and be at least 10 characters long."

        elif not username or not password or not email:
            msg = "Please fill out the form!"
        else:
            password = password.encode("utf-8")
            sha512_hash = hashlib.sha512()
            sha512_hash.update(password)
            password = sha512_hash.hexdigest()

            # Account doesn't exist and the form data is valid, now insert new account into form table
            cursor.execute(
                "INSERT INTO form (username, password, email) VALUES (%s, %s, %s)",
                (
                    username,
                    password,
                    email,
                ),
            )
           
        
   
            
 
            mysql.connection.commit() 
            
            
            attendance = attendance_taker.Face_Recognizer()
            attendance.run()
        
            if not (attendance.name != "unknown" and  attendance.name.strip()) :
             msg = "You have successfully registered!"
             
             
             cursor.execute(
                "INSERT INTO general_logs (action, time_of_action, username, password, email) VALUES (%s, %s, %s, %s, %s)",
                (
                    "Account Created",
                    current_time,
                    username,
                    password,
                    email,
                ),
            )
             
             mysql.connection.commit()
             
             get_faces_from_camera_tkinter.main()
             features_extraction_to_csv.main()
             otp_code = otp_sender.otp_send(email)
             return render_template("otp.html",otp_code=otp_code)
            else :
                
                    return render_template("register.html", msg="You have already account")       
            
    elif request.method == "POST":
        # Form is empty... (no POST data)
        msg = "Please fill out the form!"
    # Show registration form with message (if any)
    return render_template("register.html", msg=msg)



@app.route('/tools')
def tools():
    return render_template('Tools.html')

@app.route('/legal')
def legal():
    return render_template('legal.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/about')
def about():
    return render_template('about.html')
  

if __name__ == "__main__":
     
    #print (generate_otp())
    app.run(debug=True)

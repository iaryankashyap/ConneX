import mysql.connector as sq

import smtplib
import random
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)

loginpage = "login.html"
signuppage = "signup.html"


def checkuser(username):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    cursor.execute("SELECT * FROM users")
    for i in cursor:
        if i[0] == username:
            sqcon.close()
            return False
    sqcon.close()
    return True


def checkemail(email):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    cursor.execute("SELECT * FROM users")
    for i in cursor:
        if i[2] == email:
            sqcon.close()
            return False
    sqcon.close()
    return True


def register(username, password, email):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    query = "INSERT INTO users(username,password,email) VALUES ('" + \
        username+"','"+password+"','"+email+"')"
    cursor.execute(query)
    sqcon.commit()
    sqcon.close()


def log_check(username, password):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    cursor.execute("SELECT * FROM users")
    for i in cursor:
        if i[0] == username:
            if i[1] == password:
                sqcon.close()
                return True
    sqcon.close()
    return False


@app.route("/")
def login():
    return render_template(loginpage)


@app.route("/signup")
def signup():
    return render_template(signuppage)


@app.route("/login_details", methods=["GET", "POST"])
def login_details():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if log_check(username, password):
            return render_template("homepage.html")
        else:
            return render_template("loginfail.html")


@app.route("/otp", methods=["GET", "POST"])
def otppg():
    if request.method == "POST":

        if len(request.form.get("password")) > 7:
            if checkuser(request.form.get("username")):
                if checkemail(request.form.get("email")):
                    global username
                    global password
                    global email

                    username = request.form.get("username")
                    password = request.form.get("password")
                    email = request.form.get("email")
                    register(username, password, email)
                    return render_template("newlogin.html", error="Sign up success, Please login with your credentials.")
                else:
                    return render_template("wrongsignup.html", error="Email already registered!")
            else:
                return render_template("wrongsignup.html", error="Username not available!")
        else:
            return render_template("wrongsignup.html", error="Password must be at least 8 characters.")


# commit
'''
if __name__ == "__main__":
    app.run(debug=True)
'''

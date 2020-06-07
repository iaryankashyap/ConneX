import mysql.connector as sq

import smtplib
import random
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)

loginpage = "login.html"
signuppage = "signup.html"
'''
sqcon = sq.connect(host='connex.mysql.pythonanywhere-serconnex.mysql.pythonanywhere-services.com', database='connex$users',
                   user='connex', password='rootrootroot')
cursor = sqcon.cursor()
cursor.execute(
    "CREATE TABLE users(username varchar(255), password varchar(255), email varchar(255))")
cursor.commit()
cursor.close()
'''


def send_otp(emailid, admin_email, password):
    x = random.randint(1000, 5000)
    content = "Hello there, your OTP is " + str(x) + "\n\nRegards, ConneX."
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(admin_email, password)
    server.sendmail(admin_email, emailid, content)
    server.close()
    return x


def checkuser(username):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    var = cursor.execute("SELECT * FROM users")
    for i in var:
        if i[0] == username:
            cursor.close()
            return False
    cursor.close()
    return True


def checkemail(email):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    var = cursor.execute("SELECT * FROM users")
    for i in var:
        if i[2] == email:
            cursor.close()
            return False
    cursor.close()
    return True


def register(username, password, email):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    query = "INSERT INTO users(username,password,email) VALUES ('" + \
        username+"','"+password+"','"+email+"')"
    cursor.execute(query)
    cursor.commit()
    cursor.close()


def log_check(username, password):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    var = cursor.execute("SELECT * FROM users")
    for i in var:
        if i[0] == username:
            if i[1] == password:
                cursor.close()
                return True
    cursor.close()
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
                    global x
                    username = request.form.get("username")
                    password = request.form.get("password")
                    email = request.form.get("email")

                    x = send_otp(email, "school.connex@gmail.com",
                                 "portalconnex")
                    x = str(x)

                    return render_template("otp.html")
                else:
                    return render_template("wrongsignup.html", error="Email already registered!")
            else:
                return render_template("wrongsignup.html", error="Username not available!")
        else:
            return render_template("wrongsignup.html", error="Password must be at least 8 characters.")


@app.route("/otp_details", methods=["GET", "POST"])
def passotp():
    if request.method == "POST":
        otp = request.form.get("otp")
        otp = str(otp)
        if otp == x:
            register(username, password, email)
            return render_template("newlogin.html", error="Sign up success, please login with your credentials.")
        else:
            return render_template("wrongsignup.html", error="Sorry, you entered wrong OTP.")


# commit
'''
if __name__ == "__main__":
    app.run(debug=True)
'''

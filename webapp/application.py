import sqlite3
import smtplib
import random
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)

loginpage = "login.html"
signuppage = "signup.html"


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
    db = sqlite3.connect("users.db")
    var = db.execute("SELECT * FROM users")
    for i in var:
        if i[0] == username:
            db.close()
            return False
    db.close()
    return True


def checkemail(email):
    db = sqlite3.connect("users.db")
    var = db.execute("SELECT * FROM users")
    for i in var:
        if i[2] == email:
            db.close()
            return False
    db.close()
    return True


def register(username, password, email):
    db = sqlite3.connect("users.db")
    query = "INSERT INTO users(username,password,email) VALUES ('" + \
        username+"','"+password+"','"+email+"')"
    db.execute(query)
    db.commit()
    db.close()


def log_check(username, password):
    db = sqlite3.connect("users.db")
    var = db.execute("SELECT * FROM users")
    for i in var:
        if i[0] == username:
            if i[1] == password:
                db.close()
                return True
    db.close()
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

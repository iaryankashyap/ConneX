import mysql.connector as sq

import smtplib
import random
from flask import Flask, flash, request, redirect, render_template
global logged
logged = False

app = Flask(__name__)

loginpage = "login.html"
signuppage = "signup.html"


def getusers():
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor
    sqcon.close()
    return users


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
    global logged
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "iaryankashyap" and password == "superuser2022":
            users = getusers()
            return render_template("admin.html", users=users)
        if log_check(username, password):
            logged = True
            return render_template("homepage2.html")
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


@app.route("/logout")
def logout():
    global logged
    logged = False
    return redirect("/")

# READX


gr = 0
home_main = "homev7.html"
home_dark = "home-darkv7.html"
grade_main = "gradev7.html"
grade_main_dark = "grade-darkv7.html"
contact_us = "contactv7.html"
contact_us_dark = "contact-darkv7.html"
fin = "finv7.html"
findr = "findarkv7.html"


def grade(text):
    letters = 0
    words = 0
    sentences = 0
    counter = 0

    for i in text:
        counter += 1

    for i in range(counter):
        # counts the letters using ascii code
        if (ord(text[i]) >= 65 and ord(text[i]) <= 122):
            letters += 1

        # counts the words by reading spaces
        elif (ord(text[i]) == 32 and (ord(text[i - 1]) != 33 and ord(text[i - 1]) != 46 and ord(text[i - 1]) != 63)):
            words += 1

        # counts the sentences by finding dots, exclamation marks and interrogatives
        elif (ord(text[i]) == 33 or ord(text[i]) == 46 or ord(text[i]) == 63):
            sentences += 1
            words += 1
    if words == 0:
        words = 1

    L = letters * 100 / words
    S = sentences * 100 / words
    # Coleman-Liau index is computed using the formula
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Finally outputs the result to the user
    if (index < 1):
        return "Before 1"

    elif (index >= 16):
        return "16+"

    else:
        return index


@app.route("/readx")
def home():
    if logged == True:
        return render_template(home_main)
    else:
        return render_template("newlogin.html", error="Please login to continue.")


@app.route("/home-dark")
def homedark():
    return render_template(home_dark)


@app.route("/para_details", methods=["GET", "POST"])
def detpara():
    if request.method == "POST":
        var = request.form.get("subject")
        gr = grade(var)
        return render_template(grade_main, grade=gr)


@app.route("/para_details-dark", methods=["GET", "POST"])
def detparadark():
    if request.method == "POST":
        var = request.form.get("subject")
        gr = grade(var)
        return render_template(grade_main_dark, grade=gr)


@app.route("/contact")
def cont_us():
    return render_template(contact_us)


@app.route("/contact-dark")
def cont_us_dark():
    return render_template(contact_us_dark)


@app.route("/contact_details", methods=["GET", "POST"])
def condet():
    if request.method == "POST":
        mes = request.form.get("message")
        nm = request.form.get("name")
        f = open("messages.txt", "a")
        content = "Name: "+nm+"  Message:"+mes+"\n"
        f.write(content)
        f.close()
    return render_template(fin)


@app.route("/contact_details_dark", methods=["GET", "POST"])
def condetdark():
    if request.method == "POST":
        mes = request.form.get("message")
        nm = request.form.get("name")
        f = open("messages.txt", "a")
        content = "Name: "+nm+"  Message:"+mes+"\n"
        f.write(content)
        f.close()
    return render_template(findr)

# ENKRYPT


def isstring(string):
    '''Checks if entry is a valid string'''
    for i in range(len(string)):
        if string[i].isalpha():
            pass
        else:
            return False


def encrypt(text, key="ZXCVMNBLKJFGHDSAQWEYTRUIOP"):
    '''Encrypts the normal text as per the key'''
    if len(key) != 26 or key.isupper() == False or isstring(text) == False:
        return "Invalid Text, please remove numbers,symbols or spaces"
    else:
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cipher_text = ""
        key_list = list(key)
        normal_list = list(normal)
        new_plain = text.upper()

        for i in range(len(new_plain)):
            if new_plain[i].isalpha():
                index = normal_list.index(new_plain[i])
                cipher_text = cipher_text + key_list[index]
            else:
                cipher_text = cipher_text + new_plain[i]
        return cipher_text


def decrypt(text, key="ZXCVMNBLKJFGHDSAQWEYTRUIOP"):
    '''Decrypts the encrypted text as per the key'''

    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plain_text = ""
    key_list = list(key)
    normal_list = list(normal)
    new_plain = text.upper()
    if len(key) != 26 or key.isupper() == False or isstring(text) == False:
        print("KeyError: Key is not valid")
        return
    else:
        for i in range(len(text)):
            if new_plain[i].isalpha():
                index = key_list.index(new_plain[i])
                plain_text = plain_text + normal_list[index]
            else:
                plain_text = plain_text + new_plain[i]
        return plain_text


@app.route("/enkrypt")
def homeencry():
    if logged == True:
        return render_template("en-home.html")
    else:
        return render_template("newlogin.html", error="Please login to continue")


@app.route("/enkrypt_details", methods=["GET", "POST"])
def detencry():
    if request.method == "POST":
        text = request.form.get("text")
        radio = request.form.get("gridRadios")
        print(text, radio)
        if radio == "encrypt":
            fin = encrypt(text)
            return render_template("en-result.html", result=fin)
        else:
            fin = decrypt(text)
            return render_template("en-result.html", result=fin)
    return render_template("en-home.html")

# commit


'''
if __name__ == "__main__":
    app.run(debug=True)
'''

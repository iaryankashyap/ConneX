import mysql.connector as sq
# from chatbot import chatbot

import random
from flask import Flask, flash, request, redirect, render_template
global logged
logged = False
global username

app = Flask(__name__)
app.static_folder = 'static'
loginpage = "login.html"
signuppage = "signup.html"



def getusers():
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    users = []
    cursor.execute("SELECT * FROM users")
    for i in cursor:
        users.append(i[0])
    sqcon.close()
    return users


def getemails():
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    emails = []
    cursor.execute("SELECT * FROM users")
    for i in cursor:
        emails.append(i[2])
    sqcon.close()
    return emails


def usercoun():
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    for i in cursor:
        p = i[0]
    usercount = p
    sqcon.close()
    return usercount


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


def getmessage(username, email, add1, add2, zipp, city, state):

    f = open("messageconnex.txt", "a")
    temp = "Username:"+username+"\nE-mail:"+email+"\nAddress:"
    temp2 = add1 + "\nAddress2:"+add2+"\nCity:"+city+"\nState:"
    content = temp+temp2+state+"\nZip Code:"+zipp+"\n\n"
    f.write(content)
    f.close()
    return


def getcon():
    f = open("messageconnex.txt", "r")
    data = f.read()
    f.close()
    return data


@app.route("/")
def land():
    return render_template("landingfin.html")

@app.route("/records")
def records():
    return render_template("Records.html")

# @app.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(chatbot.get_response(userText))

@app.route("/login")
def login():
    return render_template(loginpage)


@app.route("/signup")
def signup():
    return render_template(signuppage)


@app.route("/login_details", methods=["GET", "POST"])
def login_details():
    global logged
    global username
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # if username == "iaryankashyap" and password == "superuser2022":
        #     logged = True
        #     users = getusers()
        #     usercount = usercoun()
        #     emails = getemails()
        #     data = getcon()
        #     return render_template("admin.html", users=users, usercount=usercount, data=data, emails=emails, nm="Aryan")
        # if username == "LMxD" and password == "lmxd12345":
        #     logged = True
        #     users = getusers()
        #     usercount = usercoun()
        #     emails = getemails()
        #     data = getcon()
        #     return render_template("admin.html", users=users, usercount=usercount, data=data, emails=emails, nm="Lakshay")
        if log_check(username, password):
            logged = True
            return redirect("/homepage_connex")
        else:
            return render_template("loginfail.html")


# @app.route("/connex_contact")
# def concontct():
#     return render_template("connexcontact.html")


@app.route("/forgot_connex")
def conforget():
    return render_template("forgot.html")


@app.route("/forgot_details", methods=["GET", "POST"])
def fordet():
    if request.method == "POST":
        username2 = request.form.get("username")
        email2 = request.form.get("email")
        password2 = request.form.get("newpassword")
        if checkuser(username2) == False and checkemail(email2) == False:
            regnewpass(username2, password2)
            return render_template("newlogin.html", error="Your Password changed successfully, please login with your new credentials.")

        else:
            return render_template("newlogin.html", error="Sorry, no such username or email found in database.")


def regnewpass(username2, password2):
    sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                       user='connex', password='rootrootroot')
    cursor = sqcon.cursor()
    query = "UPDATE users SET password='" + \
        password2+"' WHERE username='"+username2+"'"
    cursor.execute(query)
    sqcon.commit()
    sqcon.close()


@app.route("/connex_contact_submit", methods=["GET", "POST"])
def condetconnex():
    if request.method == "POST":
        username = request.form.get("username")
        add1 = request.form.get("add1")
        email = request.form.get("email")
        add2 = request.form.get("add2")
        city = request.form.get("city")
        state = request.form.get("state")
        zipp = request.form.get("zipp")
        getmessage(username, email, add1, add2, zipp, city, state)
        return render_template("consuc.html", name=username)


@app.route("/homepage_connex")
def conhome():
    if logged == True:
        return render_template("homepage2.html",username=username)
    else:
        return render_template("newlogin.html", error="Please login to continue.")


# @app.route("/admin_home")
# def adhome():
#     return render_template("homepage2.html")


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

    
@app.route("/tweets")
def twee():
    return render_template("tweets.html")
    

# # READX


# gr = 0
# home_main = "homev7.html"
# home_dark = "home-darkv7.html"
# grade_main = "gradev7.html"
# grade_main_dark = "grade-darkv7.html"
# contact_us = "contactv7.html"
# contact_us_dark = "contact-darkv7.html"
# fin = "finv7.html"
# findr = "findarkv7.html"


# def grade(text):
#     letters = 0
#     words = 0
#     sentences = 0
#     counter = 0

#     for i in text:
#         counter += 1

#     for i in range(counter):
#         # counts the letters using ascii code
#         if (ord(text[i]) >= 65 and ord(text[i]) <= 122):
#             letters += 1

#         # counts the words by reading spaces
#         elif (ord(text[i]) == 32 and (ord(text[i - 1]) != 33 and ord(text[i - 1]) != 46 and ord(text[i - 1]) != 63)):
#             words += 1

#         # counts the sentences by finding dots, exclamation marks and interrogatives
#         elif (ord(text[i]) == 33 or ord(text[i]) == 46 or ord(text[i]) == 63):
#             sentences += 1
#             words += 1
#     if words == 0:
#         words = 1

#     L = letters * 100 / words
#     S = sentences * 100 / words
#     # Coleman-Liau index is computed using the formula
#     index = round(0.0588 * L - 0.296 * S - 15.8)

#     # Finally outputs the result to the user
#     if (index < 1):
#         return "Before 1"

#     elif (index >= 16):
#         return "16+"

#     else:
#         return index


# @app.route("/readx")
# def home():
#     if logged == True:
#         return render_template(home_main)
#     else:
#         return render_template("newlogin.html", error="Please login to continue.")


# @app.route("/home-dark")
# def homedark():
#     return render_template(home_dark)


# @app.route("/para_details", methods=["GET", "POST"])
# def detpara():
#     if request.method == "POST":
#         var = request.form.get("subject")
#         gr = grade(var)
#         return render_template(grade_main, grade=gr)


# @app.route("/para_details-dark", methods=["GET", "POST"])
# def detparadark():
#     if request.method == "POST":
#         var = request.form.get("subject")
#         gr = grade(var)
#         return render_template(grade_main_dark, grade=gr)


# @app.route("/contact")
# def cont_us():
#     return render_template(contact_us)


# @app.route("/contact-dark")
# def cont_us_dark():
#     return render_template(contact_us_dark)


# @app.route("/contact_details", methods=["GET", "POST"])
# def condet():
#     if request.method == "POST":
#         mes = request.form.get("message")
#         nm = request.form.get("name")
#         f = open("messages.txt", "a")
#         content = "Name: "+nm+"  Message:"+mes+"\n"
#         f.write(content)
#         f.close()
#     return render_template(fin)


# @app.route("/contact_details_dark", methods=["GET", "POST"])
# def condetdark():
#     if request.method == "POST":
#         mes = request.form.get("message")
#         nm = request.form.get("name")
#         f = open("messages.txt", "a")
#         content = "Name: "+nm+"  Message:"+mes+"\n"
#         f.write(content)
#         f.close()
#     return render_template(findr)

# # ENKRYPT


# def isstring(string):
#     '''Checks if entry is a valid string'''
#     for i in range(len(string)):
#         if string[i].isalpha():
#             pass
#         else:
#             return False


# def encrypt(text, key="ZXCVMNBLKJFGHDSAQWEYTRUIOP"):
#     '''Encrypts the normal text as per the key'''
#     if len(key) != 26 or key.isupper() == False or isstring(text) == False:
#         return "Invalid Text, please remove numbers,symbols or spaces"
#     else:
#         normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#         cipher_text = ""
#         key_list = list(key)
#         normal_list = list(normal)
#         new_plain = text.upper()

#         for i in range(len(new_plain)):
#             if new_plain[i].isalpha():
#                 index = normal_list.index(new_plain[i])
#                 cipher_text = cipher_text + key_list[index]
#             else:
#                 cipher_text = cipher_text + new_plain[i]
#         return cipher_text


# def decrypt(text, key="ZXCVMNBLKJFGHDSAQWEYTRUIOP"):
#     '''Decrypts the encrypted text as per the key'''

#     normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     plain_text = ""
#     key_list = list(key)
#     normal_list = list(normal)
#     new_plain = text.upper()
#     if len(key) != 26 or key.isupper() == False or isstring(text) == False:
#         print("KeyError: Key is not valid")
#         return
#     else:
#         for i in range(len(text)):
#             if new_plain[i].isalpha():
#                 index = key_list.index(new_plain[i])
#                 plain_text = plain_text + normal_list[index]
#             else:
#                 plain_text = plain_text + new_plain[i]
#         return plain_text


# @app.route("/enkrypt")
# def homeencry():
#     global logged
#     if logged == True:
#         return render_template("en-home.html")
#     else:
#         return render_template("newlogin.html", error="Please login to continue")


# @app.route("/enkrypt_details", methods=["GET", "POST"])
# def detencry():
#     if request.method == "POST":
#         text = request.form.get("text")
#         radio = request.form.get("gridRadios")
#         print(text, radio)
#         if radio == "encrypt":
#             fin = encrypt(text)
#             return render_template("en-result.html", result=fin)
#         else:
#             fin = decrypt(text)
#             return render_template("en-result.html", result=fin)
#     return render_template("en-home.html")


# # TODOList

# @app.route('/todo')
# def todocon():
#     return render_template("todolist.html")


# Debugging Statements

# if __name__ == "__main__":
#     app.run(debug=True)


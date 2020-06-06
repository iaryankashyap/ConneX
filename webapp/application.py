import cs50
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)

loginpage = "login.html"
signuppage = "signup.html"


def checkuser(username):
    db = SQL("sqlite:///users.db")
    var = db.execute("SELECT * FROM users")
    for i in range(len(var)):
        if var[i]["username"] == username:
            return False
    return True


def register(username, password):
    db = SQL("sqlite:///users.db")
    db.execute("INSERT INTO users(username,password) VALUES (:username,:password)",
               username=username, password=password)


def log_check(username, password):
    db = SQL("sqlite:///users.db")
    var = db.execute("SELECT * FROM users")
    for i in range(len(var)):
        if var[i]["username"] == username:
            if var[i]["password"] == password:
                return True
    return False


def submit_record(admission, name, classs, marks):
    db = SQL("sqlite:///users.db")
    db.execute("INSERT INTO records(admission,name,classs,marks) VALUES (:admission,:name,:classs,:marks)",
               admission=admission, name=name, classs=classs, marks=marks)


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


@app.route("/signup_details", methods=["GET", "POST"])
def sign_check():
    if request.method == "POST":

        if len(request.form.get("password")) > 7:
            if checkuser(request.form.get("username")):

                mess = "Signed up successfully, please login with your credentials."
                username = request.form.get("username")
                password = request.form.get("password")
                register(username, password)
                return render_template("newlogin.html", error=mess)
            else:
                return render_template("wrongsignup.html", error="Username not available!")
        else:
            return render_template("wrongsignup.html", error="Password must be at least 8 characters.")


'''
if __name__ == "__main__":
    app.run(debug=True)
'''

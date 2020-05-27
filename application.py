from cs50 import SQL
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)


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


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login-dark")
def darklogin():
    return render_template("login-dark.html")


@app.route("/signup-dark")
def darksignup():
    return render_template("signup-dark.html")


@app.route("/login_details", methods=["GET", "POST"])
def login_details():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if log_check(username, password):
            return redirect("sample.html")
        else:
            return render_template("/signup")


@app.route("/signup_details", methods=["GET", "POST"])
def sign_check():
    if request.method == "POST":
        if request.form.get("password") == request.form.get("password2"):
            if len(request.form.get("password")) > 7:
                if checkuser(request.form.get("username")):
                    username = request.form.get("username")
                    password = request.form.get("password")
                    register(username, password)
                    return render_template("login.html")
                else:
                    return render_template("signupfail.html", error="Username not available!")
            else:
                return render_template("signupfail.html", error="Password must be at least 8 characters.")
        else:
            return render_template("signupfail.html", error="Passwords do not match")


if __name__ == "__main__":
    app.run(debug=True)

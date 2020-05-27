from cs50 import SQL
from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)



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


if __name__ == "__main__":
    app.run(debug=True)

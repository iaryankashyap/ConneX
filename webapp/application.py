from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)

loginpage = "login.html"
signuppage = "signup.html"


@app.route("/")
def login():
    return render_template(loginpage)


@app.route("/signup")
def signup():
    return render_template(signuppage)

'''
if __name__ == "__main__":
    app.run(debug=True)
'''
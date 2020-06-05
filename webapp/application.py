from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("main.html")


'''
if __name__ == "__main__":
    app.run(debug=True)
'''

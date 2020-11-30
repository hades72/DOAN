from flask import Flask
from mainapp import app
from mainapp.admin_module import *

@app.route("/")
def home():
    return "Hello! <h1>Nguyen Truong Thinh</h1>"

@app.route("/<abc>")
def user(abc):
    return f"{ abc } <h1>Truong Thinh</h1>"

if __name__ == "__main__":
    app.run(port=8900, debug=True)
from flask import Flask, render_template
from mainapp import app
from mainapp.admin_module import *

@app.route("/")
def home():
    return f"<h1>dasdasd</h1>"


if __name__ == "__main__":
    app.run(port=8900, debug=True)
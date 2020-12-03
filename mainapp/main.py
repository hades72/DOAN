from datetime import time

from flask import Flask, render_template, redirect, request
from flask_login import login_user
from mainapp import app, login
from mainapp.admin_module import *
from mainapp.model import User
import hashlib


@app.route("/")
def home():
    return f"<h1>Bán vé máy bay</h1>"

@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            login_user(user=user)
        else:
            err_msg = 'Dang nhap that bai'
    return redirect("/admin")

@app.route("/revenue")
def chart():
    return render_template('admin/revenue.html')

@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(port=8900, debug=True)
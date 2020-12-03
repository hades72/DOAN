from datetime import time
import smtplib
from socket import gaierror
from sqlalchemy.sql import TableClause
import ultis
from mainapp import db
from flask import Flask, render_template, redirect, request, json
from flask_login import login_user
from mainapp import app, login
from mainapp.admin_module import *
from mainapp.model import User, Flight, FlightRoute, Airport, Intermediarie_AirPort, Plane_TicketType
from sqlalchemy import insert
import hashlib
import cgi
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login", methods = ['POST','GET'])
def user_login():
    err_msg = ""
    user = []
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        user = User.query.filter(User.username == _username, User.password == _password).first()
        if user:
            if user.check_role() == 3:
                print(user.Id)
                return redirect('/user/' + str(user.Id))
            else:
                return redirect('/admin')
        else:
            err_msg = 'Fail to login'
    return render_template('login.html', user=user)
@app.route("/user/<Id>", methods = ['GET','POST'])
def user(Id):
    user = User.query.filter(User.Id == Id).first()
    return render_template('user/index.html', user=user)
@app.route("/received_flight", methods = ['GET','POST'])
def received_flight():
    return render_template('received_flight.html')
@app.route("/book_flight")
def book_flight():
    return render_template('book_flight.html')

@app.route("/search_flight",methods = ['GET','POST'])
def search_flight():
    list_flights = []
    flights = []
    if request.method == 'POST':
        _flyingFrom = request.form['flyingFrom']
        _flyingTo = request.form['flyingTo']
        _dateStart = request.form['dateStart']
        if _flyingFrom and _flyingTo and _dateStart:
            idFrom = ultis.find_airport_by_name(_flyingFrom)
            idTo = ultis.find_airport_by_name(_flyingTo)
            if idFrom and idTo:
                flights = ultis.get_flights_by_3nd(idFrom.Id, idTo.Id, _dateStart)
        elif _flyingTo and _flyingFrom:
            idFrom = ultis.find_airport_by_name(_flyingFrom)
            idTo = ultis.find_airport_by_name(_flyingTo)
            if idFrom and idTo:
                flights = ultis.get_flights_by_2nd(idFrom.Id, idTo.Id)
            else:
                flights = []
        elif _flyingFrom and _dateStart:
            idFrom = ultis.find_airport_by_name(_flyingFrom)
            if idFrom:
                flights = ultis.get_flights_by_From_date(idFrom.Id, _dateStart)
        elif _flyingTo and _dateStart:
            idTo = ultis.find_airport_by_name(_flyingTo)
            if idTo:
                flights = ultis.get_flights_by_to_date(idTo.Id, _dateStart)
        elif _flyingTo or _flyingFrom or _dateStart:
            idFrom = ultis.find_airport_by_name(_flyingFrom)
            idTo = ultis.find_airport_by_name(_flyingTo)
            if idFrom:
                flights = ultis.find_by_id_from(idFrom.Id)
            elif idTo:
                flights = ultis.find_by_id_to(idTo.Id)
            elif _dateStart:
                flights = ultis.find_by_date(_dateStart)
        else:
            flights = []
    else:
        flights = ultis.get_flights()

    for f in flights:
        stt = 0
        list_airport = []
        list_ticket_type = []
        a = Airport.query.add_columns(Airport.Name).filter(f.Origin_Id == Airport.Id).one()
        b = Airport.query.add_columns(Airport.Name).filter(f.Destination_Id == Airport.Id).one()
        airports = Intermediarie_AirPort.query.filter(f.Id == Intermediarie_AirPort.FlightRoute_Id).all()
        plane = Plane_TicketType.query.filter(f.Plane_Id == Plane_TicketType.Plane_Id).all()
        for p in plane:
            plane_details = {
                "Name": p.TicketType,
                "Quantity": p.Quantity
            }
            list_ticket_type.append(plane_details)
        for air in airports:
            stt += 1
            air_name = Airport.query.filter(air.Airport_Id == Airport.Id).one()
            airports_details = {
                "STT": stt,
                "Airport_Name": air_name.Name,
                "WaitingTime": air.WaitingTime,
                "Note": air.Note
            }
            list_airport.append(airports_details)
        dic = {
            "Id" : f.Id,
            "FlightDate" : f.FlightDate,
            "FlightTime" : f.FlightTime,
            "Origin" : a.Name,
            "Destination" : b.Name,
            "listAirport": list_airport,
            "listTicket": list_ticket_type
        }
        list_flights.append(dic)
    return render_template('search_flight.html', list_flight=list_flights)
@app.route("/signup", methods = ['POST'])
def signup():
    _name = request.form['fullname']
    _username = request.form['username']
    _password = request.form['psw']
    _email = request.form['email']
    _cmnd = request.form['cmnd']
    _phone = request.form['phone']
    user = User(FullName=_name, username=_username, password=_password, RoleID=3, CMND=_cmnd, Email=_email, PhoneNumber=_phone)
    print(user)
    db.session.add(user)
    db.session.commit()
    return render_template('/login.html')
@app.route("/register", methods = ['GET','POST'])
def register():
    return render_template('/register.html')
# @app.route("/login-admin", methods=['GET', 'POST'])
# def login_admin():
#     err_msg = ''
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         # password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
#         user = User.query.filter(User.username == username, User.password == password).first()
#         if user:
#             login_user(user=user)
#         else:
#             err_msg = 'Dang nhap that bai'
#     return redirect("/admin")

@app.route("/revenue")
def chart():
    return render_template('admin/revenue.html')

@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(port=8900, debug=True)
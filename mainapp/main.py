from flask import Flask, render_template, redirect, request, json, url_for, session
from mainapp import app, login, ultis
from mainapp.admin_module import *
from mainapp.model import User, Flight, FlightRoute, Airport, Intermediarie_AirPort, Plane_TicketType, Ticket
import hashlib
from functools import wraps
def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for('user_login', next=request.url))
        return f(*args, **kwargs)
    return check
@app.route("/history",methods=['GET','POST'])
@login_required
def history():
    print(session['user'])
    if session['user']['RoleId'] != 1 and session['user']['RoleId'] != 2:
        return redirect(url_for('search_flight'))
    msg = ''
    list_ticket = []
    tickets = Ticket.query.filter().all()
    for t in tickets:
        flight_name = ""
        flight_time = ""
        flight_date = ""
        user = User.query.filter(t.User_Id == User.Id).first()
        flights = ultis.get_flights()
        for f in flights:
            if f.Plane_Id == t.Plane_Id:
                flight_name = f.Description
                flight_time = f.TimeStart
                flight_date = f.FlightDate
        ticket = TicketType.query.filter(TicketType.Id == t.TicketType_Id).first()
        dic = {
            "Id": t.Id,
            "name": user.FullName,
            "flightname": flight_name,
            "phone": user.PhoneNumber,
            "time": flight_time,
            "date": flight_date,
            "typeticket": ticket.Name,
            "price": ticket.Price
        }
        list_ticket.append(dic)
    return render_template('history.html', list_ticket=list_ticket)
@app.route("/delete_ticket/<id>", methods = ['GET', 'POST'])
def delete_ticket(id):
    msg = ""
    Ticket.query.filter(Ticket.Id == id).delete()
    db.session.commit()
    return redirect(url_for('history'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    msg = ''
    if request.method == 'POST':
        _name = request.form['fullname']
        _email = request.form['email']
        _CMND = request.form['cmnd']
        _phone = request.form['phone']
        user = User.query.filter(User.Id == session['user']['Id']).first()
        user.FullName = _name
        user.Email = _email
        user.PhoneNumber = _phone
        user.CMND = _CMND
        db.session.commit()
        msg = 'Succes !!!'
        _user = ultis.cv_user_to_json(user)
        session['user'] = _user
        return render_template('account.html', msg=msg)
    return render_template('account.html', msg=msg)

@app.route("/login", methods = ['POST','GET'])
def user_login():
    if request.method == 'POST':
        err_msg = ""
        user = []
        _username = request.form['username']
        _password = request.form['password']
        _password = hashlib.md5(_password.encode("utf-8")).hexdigest()
        user = User.query.filter(User.username == _username, User.password == _password).first()
        if user:
            _user = ultis.cv_user_to_json(user)
            session['user'] = _user
            if "next" in request.args:
                return redirect(request.args["next"])
            return redirect('/')
        else:
            err_msg = 'Fail to login'
        return render_template('login.html', user=user, err_msg=err_msg)
    return render_template('login.html')
@app.route("/logout", methods=['GET','POST'])
def logout():
    session['user'] = None
    return redirect('/')
@app.route("/received_flight", methods = ['GET','POST'])
def received_flight():

    msg = ''
    session['flight_route'] = []
    list_flight = []
    flights = ultis.get_flights()

    for f in flights:
        total_ticket = 0
        stt = 0
        ticket = Ticket.query.filter(f.Plane_Id == Ticket.Plane_Id).all()
        list_airport = []
        list_ticket_type = []
        a = Airport.query.add_columns(Airport.Name).filter(f.Origin_Id == Airport.Id).one()
        b = Airport.query.add_columns(Airport.Name).filter(f.Destination_Id == Airport.Id).one()
        airports = Intermediarie_AirPort.query.filter(f.Id == Intermediarie_AirPort.FlightRoute_Id).all()
        plane = Plane_TicketType.query.filter(f.Plane_Id == Plane_TicketType.Plane_Id).all()
        for p in plane:

            total_ticket += p.Quantity
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
            "Id": f.Id,
            "FlightDate": f.FlightDate,
            "FlightTime": f.FlightTime,
            "TimeStart": f.TimeStart,
            "Origin": a.Name,
            "Destination": b.Name,
            "listAirport": list_airport,
            "listTicket": list_ticket_type,
            "totalTicket": total_ticket,
            "ticketed": len(ticket)
        }
        list_flight.append(dic)
        print(list_flight)
    return render_template('received_flight.html', list_flight=list_flight)
@app.route("/book_flight/<id>", methods= ['GET','POST'])
@login_required
def book_flight(id):
    msg = ''
    flight = ultis.get_flights_by_id(id)
    _user = User.query.filter(User.Id == session['user']['Id']).first()
    user = ultis.cv_user_to_json(_user)
    type_tickets = Plane_TicketType.query.filter(flight.Plane_Id == Plane_TicketType.Plane_Id).all()
    tickets = []
    for i in type_tickets:
        tik = TicketType.query.filter(TicketType.Id == i.TicketType_Id).first()
        tickets.append(tik)
    if request.method == 'POST':
        _fullname = request.form['fullname']
        _flightroute = request.form['flightroute']
        _cmnd = request.form['cmnd']
        _phone = request.form['phone']
        ticket_id = request.form['ticket_id']
        plane = Plane_TicketType.query.filter(Plane_TicketType.Plane_Id == flight.Plane_Id,
                                              Plane_TicketType.TicketType_Id == ticket_id).first()
        plane.Quantity = plane.Quantity - 1
        if plane.Quantity >= 0:
            ticket = Ticket(User_Id=user['Id'], Plane_Id=flight.Plane_Id, TicketType_Id = ticket_id)
            db.session.add(ticket)
            user = User(FullName=_fullname, username=None, password=None, RoleID=4, CMND=_cmnd, Email=None,
                        PhoneNumber=_phone)
            db.session.add(user)
            db.session.commit()
            msg = 'Succes !!!'
        else:
            plane.Quantity = plane.Quantity + 1
            msg = 'Fail to book flight'

        return render_template('book_flight.html', flight=flight, user=user, tickets=tickets, msg=msg)
    return render_template('book_flight.html', flight=flight, user=user, tickets=tickets, msg=msg)

@app.route("/",methods = ['GET','POST'])
def search_flight():
    session['flight_route'] = []
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
                "Quantity": p.Quantity,
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
            "TimeStart": f.TimeStart,
            "listAirport": list_airport,
            "listTicket": list_ticket_type
        }
        list_flights.append(dic)
    return render_template('search_flight.html', list_flight=list_flights)
@app.route("/register", methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        _name = request.form['fullname']
        _username = request.form['username']
        _password = request.form['psw']
        _password = hashlib.md5(_password.encode("utf-8")).hexdigest()
        _email = request.form['email']
        _cmnd = request.form['cmnd']
        _phone = request.form['phone']
        user = User(FullName=_name, username=_username, password=_password, RoleID=3, CMND=_cmnd, Email=_email, PhoneNumber=_phone)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_login'))
    return render_template('/register.html')

@app.route("/revenue")
def chart():
    return render_template('admin/revenue.html')

@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)
if __name__ == "__main__":
    app.run(port=8900, debug=True)
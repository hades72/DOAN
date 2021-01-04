from flask import jsonify
from mainapp.model import User, Flight, FlightRoute, Airport, Intermediarie_AirPort, Plane_TicketType
from mainapp import db
def cv_user_to_json(user):
    _user = {
        "Id": user.Id,
        "FullName": user.FullName,
        "username": user.username,
        "password": user.password,
        "RoleId": user.RoleID,
        "CMND": user.CMND,
        "Email": user.Email,
        "PhoneNumber": user.PhoneNumber
    }
    return _user

def get_flights_by_3nd(idFrom, idTo, dateStart):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, FlightRoute.Origin_Id == idFrom, FlightRoute.Destination_Id == idTo, \
               Flight.FlightDate == dateStart).all()
    return flights
def get_flights_by_2nd(idFrom, idTo):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, FlightRoute.Origin_Id == idFrom,
               FlightRoute.Destination_Id == idTo).all()
    return flights
def get_flights_by_From_date(idFrom, dateStart):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, FlightRoute.Origin_Id == idFrom, dateStart == Flight.FlightDate).all()
    return flights
def get_flights_by_to_date(idTo, dateStart):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, FlightRoute.Destination_Id == idTo, dateStart == Flight.FlightDate).all()
    return flights
def get_flights():
    flights = Flight.query.join(FlightRoute).\
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime, Flight.Plane_Id).\
        filter(Flight.FlightRoute_Id == FlightRoute.Id).all()
    return flights
def get_flights_by_id(id):
    flights = Flight.query.join(FlightRoute).\
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime, Flight.Plane_Id, FlightRoute.Description).\
        filter(Flight.FlightRoute_Id == FlightRoute.Id, id == FlightRoute.Id).first()
    return flights
def find_airport_by_name(name):
    id = Airport.query.filter(name == Airport.Name).first()
    return id
def find_by_id_from(id):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, FlightRoute.Origin_Id == id).all()
    return flights
def find_by_id_to(id):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, FlightRoute.Destination_Id == id).all()
    return flights
def find_by_date(dateStart):
    flights = Flight.query.join(FlightRoute). \
        add_columns(Flight.Id, Flight.FlightDate, FlightRoute.Origin_Id, FlightRoute.Destination_Id, Flight.FlightTime,
                    Flight.Plane_Id). \
        filter(Flight.FlightRoute_Id == FlightRoute.Id, dateStart == Flight.FlightDate).all()
    return flights
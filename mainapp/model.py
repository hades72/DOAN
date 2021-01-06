from sqlalchemy import Column, Integer, Float, String, TIME, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from mainapp import db
from flask_login import UserMixin
import hashlib

class Role(db.Model):
    __tablename__ = 'Role'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    # Role has 3 type:
    # - admin
    # - seller
    # - user
    # - orther

    def __str__(self):
        return self.Name

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(50), nullable=False)
    username = Column(String(50))
    password = Column(String(50), nullable=True)
    RoleID = Column(Integer, ForeignKey(Role.Id), nullable=False)
    CMND = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=True)
    PhoneNumber = Column(String(50), nullable=True)
    Role = relationship('Role', foreign_keys=[RoleID])
    def get_id(self):
        return (self.Id)

    def __str__(self):
        return  self.FullName


class Airport(db.Model):
    __tablename__ = 'AIRPORT'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'Id': self.Id,
            'Name': self.Name
        }

    def __str__(self):
        return self.Name
class FlightRoute(db.Model):
    __tablename__ = 'FLIGHTROUTE'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Origin_Id = Column(Integer, ForeignKey(Airport.Id), nullable=False)
    Destination_Id = Column(Integer, ForeignKey(Airport.Id), nullable=False)
    Description = Column(String(100), default="")
    Origin = relationship('Airport', foreign_keys=[Origin_Id])
    # Nơi xuất phát
    Destination = relationship('Airport', foreign_keys=[Destination_Id])
    # Đích đến
    def __str__(self):
        return self.Description

class Intermediarie_AirPort(db.Model):
    __tablename__ = 'INTERMEDIARIE_AIRPORT'
    FlightRoute_Id = Column(Integer, ForeignKey(FlightRoute.Id), primary_key=True)
    Airport_Id = Column(Integer, ForeignKey(Airport.Id), primary_key=True)
    WaitingTime = Column(Integer, nullable=False)
    Note = Column(String(100), nullable=True)
    FlightRoute = relationship('FlightRoute', foreign_keys=[FlightRoute_Id])
    Airport = relationship('Airport', foreign_keys=[Airport_Id])
    def __str__(self):
        return "ASD"

class TicketType(db.Model):
    __tablename__ = 'TICKETTYPE'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Price = Column(Integer, nullable=False)
    def __str__(self):
        return self.Name
class Plane(db.Model):
    __tablename__ = 'PLANE'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    def __str__(self):
        return self.Name

class Flight(db.Model):
    __tablename__ = 'FLIGHT'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    FlightDate = Column(Date, nullable=False)
    TimeStart = Column(TIME, nullable=False)
    FlightTime = Column(Integer, nullable=False)
    Plane_Id = Column(Integer, ForeignKey(Plane.Id), nullable=False)
    FlightRoute_Id = Column(Integer, ForeignKey(FlightRoute.Id), nullable=False)

    FlightRoute = relationship('FlightRoute', foreign_keys=[FlightRoute_Id])
    Plane = relationship('Plane', foreign_keys=[Plane_Id])
    def __str__(self):
        return self.Name
class Plane_TicketType(db.Model):
    __tablename__ = 'PLANE_TICKETTYPE'
    Plane_Id = Column(Integer, ForeignKey(Plane.Id), nullable=False, primary_key=True)
    TicketType_Id = Column(Integer, ForeignKey(TicketType.Id), nullable=False,primary_key=True)
    Quantity = Column(Integer, nullable=False)
    Plane = relationship('Plane', foreign_keys=[Plane_Id])
    TicketType = relationship('TicketType', foreign_keys=[TicketType_Id])
    def __str__(self):
        return "no return"
class Ticket(db.Model):
    __tablename__ = 'TICKET'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    User_Id = Column(Integer, ForeignKey(User.Id), nullable=False)
    User = relationship('User', foreign_keys=[User_Id])
    Plane_Id = Column(Integer, ForeignKey(Plane.Id), nullable=False)
    TicketType_Id = Column(Integer, ForeignKey(TicketType.Id), nullable=False)
    TicketType = relationship('TicketType', foreign_keys=[TicketType_Id])
    Plane = relationship('Plane', foreign_keys=[Plane_Id])
    def __str__(self):
        return self.Plane

if __name__ == '__main__':
    db.create_all()
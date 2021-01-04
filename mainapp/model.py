from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mainapp import db
from datetime import datetime
from flask_login import  UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'Role'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    # Role has 3 type:
    # - admin
    # - seller
    # - passenger

    def __str__(self):
        return self.Name

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(50), nullable=False)
    username = Column(String(50), nullable=True)
    password = Column(String(50), nullable=True)
    RoleID = Column(Integer, ForeignKey(Role.Id), nullable=False)
    CMND = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=True)
    PhoneNumber = Column(String(50), nullable=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
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
# intermediarie_aiport = db.Table('intermediarie_aiport',
#                                 Column('FlightRoute_Id', Integer,
#                                        ForeignKey('FLIGHTROUTE.Id'),
#                                        primary_key=True),
#                                 Column('Airport_Id',Integer,
#                                        ))
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
    FlightTime = Column(String(10), nullable=False)
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
    Plane_Id = Column(Integer, ForeignKey(Plane.Id), nullable=False)
    User_Id = Column(Integer, ForeignKey(User.Id), nullable=False)
    TicketType_Id = Column(Integer, ForeignKey(TicketType.Id), nullable=False)
    Status = Column(Boolean, default=False)


    TicketType = relationship('TicketType', foreign_keys=[TicketType_Id])
    Plane = relationship('Plane', foreign_keys=[Plane_Id])
    User = relationship('User', foreign_keys=[User_Id])
    def __str__(self):
        return self.Id

if __name__ == '__main__':
    db.create_all()
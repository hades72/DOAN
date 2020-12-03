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
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    RoleID = Column(Integer, ForeignKey(Role.Id), nullable=False)
    CMND = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=True)
    PhoneNumber = Column(String(50),nullable=True)
    def check_role  (self):
        return self.RoleID
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
class Seat(db.Model):
    __tablename__ = 'SEAT'
    Id = Column(Integer, primary_key=True,autoincrement=True)
    Plane_Id = Column(Integer, ForeignKey(Plane.Id), nullable=False)
    TicketType_Id = Column(Integer, ForeignKey(TicketType.Id), nullable=False)
    Status = Column(Boolean, default=False)


    Plane = relationship('Plane', foreign_keys=[Plane_Id])
    TicketType = relationship('TicketType', foreign_keys=[TicketType_Id])
    def __str__(self):
        return self.Id

class Ticket(db.Model):
    __tablename__ = 'TICKET'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Plane_Id = Column(Integer, ForeignKey(Plane.Id), nullable=False)
    Seat_Id = Column(Integer, ForeignKey(Seat.Id), nullable=False)
    User_Id = Column(Integer, ForeignKey(User.Id), nullable=False)


    Plane = relationship('Plane', foreign_keys=[Plane_Id])
    Seat = relationship('Seat', foreign_keys=[Seat_Id])
    User = relationship('User', foreign_keys=[User_Id])
    def __str__(self):
        return self.Id

# class HoaDon(db.Model):
#     __tablename__ = 'HOADON'
#
#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     ThanhTien = Column(Float, nullable=False)
#     NgayLap = Column(Date, default=datetime.now(), nullable=False)
#     IdNhanVien = Column(Integer, ForeignKey(NhanVien.Id), nullable=False)
#     IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
#
#     NhanVien = relationship('NhanVien', foreign_keys=[IdNhanVien])
#     KhachHang = relationship('KhachHang', foreign_keys=[IdKhachHang])
#
#     def __str__(self):
#         return self.ThanhTien
#
#
#
# class PhieuDatCho(db.Model):
#     __tablename__ = 'PHIEUDATCHO'
#
#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     NgayDat = Column(Date, default=datetime.now(), nullable=False)
#     SoGhe = Column(String(10), nullable=False)
#     IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
#     IdChuyenBay = Column(Integer, ForeignKey(ChuyenBay.Id), nullable=False)
#     IdHangVe = Column(Integer, ForeignKey(HangVe.Id), nullable=False)
#
#     KhachHang = relationship('KhachHang', foreign_keys=[IdKhachHang])
#     ChuyenBay = relationship('ChuyenBay', foreign_keys=[IdChuyenBay])
#     HangVe = relationship('HangVe', foreign_keys=[IdHangVe])
#
#     def __str__(self):
#         return self.Id

# class VeChuyenBayKhachHang(db.Model):
#     __tablename__ = 'VECHUYENBAY_KHACHHANG'
#
#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     IdVeChuyenBay = Column(Integer, ForeignKey(VeChuyenBay.Id), nullable=False)
#     IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
#     Description = Column(String(100), nullable=True)
#
#     VeChuyenBay = relationship('VeChuyenBay', foreign_keys=[IdVeChuyenBay])
#     KhachHang = relationship('KhachHang', foreign_keys=[IdKhachHang])

# class NhanVien(db.Model):
#     __tablename__ = 'NHANVIEN'
#
#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     TenNhanVien = Column(String(100), nullable=True)
#
#     def __str__(self):
#         return self.TenNhanVien

# class KhachHang(db.Model):
#     __tablename__ = 'KHACHHANG'
#
#     CMND = Column(Integer, primary_key=True)
#     TenKhachHang = Column(String(100), nullable=False)
#     GioiTinh = Column(String(10), nullable=True)
#     SoDienThoai = Column(String(15), nullable=False)
#     DiaChi = Column(String(200), nullable=True)
#     GhiChu = Column(String(100), nullable=True)
#
#     def __str__(self):
#         return self.TenKhachHang

if __name__ == '__main__':
    db.create_all()
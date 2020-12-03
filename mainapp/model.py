from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mainapp import db
from datetime import datetime
from flask_login import  UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return  self.Name

class SanBay(db.Model):
    __tablename__ = 'SANBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TenSanBay = Column(String(50), nullable=False)

    def __str__(self):
        return self.TenSanBay

class TuyenBay(db.Model):
    __tablename__ = 'TUYENBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdSanBayDi = Column(Integer, ForeignKey(SanBay.Id), nullable=False)
    IdSanBayDen = Column(Integer, ForeignKey(SanBay.Id), nullable=False)
    Description = Column(String(100), nullable=True)

    SanBayDi = relationship('SanBay', foreign_keys=[IdSanBayDi])
    SanBayDen = relationship('SanBay', foreign_keys=[IdSanBayDen])

    def __str__(self):
        return self.Description

class NhanVien(db.Model):
    __tablename__ = 'NHANVIEN'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TenNhanVien = Column(String(100), nullable=True)

    def __str__(self):
        return self.TenNhanVien

class KhachHang(db.Model):
    __tablename__ = 'KHACHHANG'

    CMND = Column(Integer, primary_key=True)
    TenKhachHang = Column(String(100), nullable=False)
    GioiTinh = Column(String(10), nullable=True)
    SoDienThoai = Column(String(15), nullable=False)
    DiaChi = Column(String(200), nullable=True)
    GhiChu = Column(String(100), nullable=True)

    def __str__(self):
        return self.TenKhachHang

class DonGia(db.Model):
    __tablename__ = 'DONGIA'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Gia = Column(Float, nullable=False)

    def __str__(self):
        return self.Gia

class ChuyenBay(db.Model):
    __tablename__ = 'CHUYENBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    NgayGio = Column(Date, nullable=False)
    SoGhe = Column(String(5), nullable=False)
    IdTuyenBay = Column(Integer, ForeignKey(TuyenBay.Id), nullable=False)

    TuyenBay = relationship('TuyenBay', foreign_keys=[IdTuyenBay])

    def __str__(self):
        return self.TuyenBay

class MayBay(db.Model):
    __tablename__ = 'MAYBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    LoaiMayBay = Column(String(50), nullable=False)

    def __str__(self):
        return self.LoaiMayBay

class HoaDon(db.Model):
    __tablename__ = 'HOADON'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ThanhTien = Column(Float, nullable=False)
    NgayLap = Column(Date, default=datetime.now(), nullable=False)
    IdNhanVien = Column(Integer, ForeignKey(NhanVien.Id), nullable=False)
    IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)

    NhanVien = relationship('NhanVien', foreign_keys=[IdNhanVien])
    KhachHang = relationship('KhachHang', foreign_keys=[IdKhachHang])

    def __str__(self):
        return self.ThanhTien

class VeChuyenBay(db.Model):
    __tablename__ = 'VECHUYENBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TrangThai = Column(String(20), nullable=False)
    IdDonGia = Column(Integer, ForeignKey(DonGia.Id), nullable=False)
    IdChuyenBay = Column(Integer, ForeignKey(ChuyenBay.Id), nullable=False)

    DonGia = relationship('DonGia', foreign_keys=[IdDonGia])
    ChuyenBay = relationship('ChuyenBay', foreign_keys=[IdChuyenBay])


class HangVe(db.Model):
    __tablename__ = 'HANGVE'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TenHangVe = Column(String(50), nullable=False)
    IdVeChuyenBay = Column(Integer, ForeignKey(VeChuyenBay.Id), nullable=False)

    VeChuyenBay = relationship('VeChuyenBay', foreign_keys=[IdVeChuyenBay])

    def __str__(self):
        return self.TenHangVe

class PhieuDatCho(db.Model):
    __tablename__ = 'PHIEUDATCHO'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    NgayDat = Column(Date, default=datetime.now(), nullable=False)
    SoGhe = Column(String(10), nullable=False)
    IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
    IdChuyenBay = Column(Integer, ForeignKey(ChuyenBay.Id), nullable=False)
    IdHangVe = Column(Integer, ForeignKey(HangVe.Id), nullable=False)

    KhachHang = relationship('KhachHang', foreign_keys=[IdKhachHang])
    ChuyenBay = relationship('ChuyenBay', foreign_keys=[IdChuyenBay])
    HangVe = relationship('HangVe', foreign_keys=[IdHangVe])

class VeChuyenBayKhachHang(db.Model):
    __tablename__ = 'VECHUYENBAY_KHACHHANG'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdVeChuyenBay = Column(Integer, ForeignKey(VeChuyenBay.Id), nullable=False)
    IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
    Description = Column(String(100), nullable=True)

    VeChuyenBay = relationship('VeChuyenBay', foreign_keys=[IdVeChuyenBay])
    KhachHang = relationship('KhachHang', foreign_keys=[IdKhachHang])


if __name__ == '__main__':
    db.create_all()
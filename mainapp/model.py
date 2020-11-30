from xmlrpc.client import DateTime

from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mainapp import db
from datetime import datetime

class SanBay(db.Model):
    __tablename__ = 'SANBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TenSanBay = Column(String(50), nullable=False)
    Tuyenbay = relationship('TuyenBay', backref='SANBAY', lazy=True)

    def __str__(self):
        return self.TenSanBay

class TuyenBay(db.Model):
    __tablename__ = 'TUYENBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdSanBayDi = Column(Integer, ForeignKey(SanBay.Id), nullable=False)
    # IdSanBayDen = Column(Integer, ForeignKey(SanBay.Id), nullable=False)
    Description = Column(String(100), nullable=True)

class NhanVien(db.Model):
    __tablename__ = 'NHANVIEN'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TenNhanVien = Column(String(100), nullable=True)

class KhachHang(db.Model):
    __tablename__ = 'KHACHHANG'

    CMND = Column(Integer, primary_key=True)
    TenKhachHang = Column(String(100), nullable=False)
    GioiTinh = Column(String(10), nullable=True)
    SoDienThoai = Column(String(15), nullable=False)
    DiaChi = Column(String(200), nullable=True)
    GhiChu = Column(String(100), nullable=True)

class DonGia(db.Model):
    __tablename__ = 'DONGIA'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Gia = Column(Float, nullable=False)

class ChuyenBay(db.Model):
    __tablename__ = 'CHUYENBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    NgayGio = Column(Date, nullable=False)
    SoGhe = Column(String(5), nullable=False)
    IdTuyenBay = Column(Integer, ForeignKey(TuyenBay.Id), nullable=False)

class MayBay(db.Model):
    __tablename__ = 'MAYBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    LoaiMayBay = Column(String(50), nullable=False)
    IdChuyenBay = Column(Integer, ForeignKey(ChuyenBay.Id), nullable=True)

class HoaDon(db.Model):
    __tablename__ = 'HOADON'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ThanhTien = Column(Float, nullable=False)
    NgayLap = Column(Date, default=datetime.now(), nullable=False)
    IdNhanVien = Column(Integer, ForeignKey(NhanVien.Id), nullable=False)
    IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)

class VeChuyenBay(db.Model):
    __tablename__ = 'VECHUYENBAY'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TrangThai = Column(String(20), nullable=False)
    IdDonGia = Column(Integer, ForeignKey(DonGia.Id), nullable=False)
    IdChuyenBay = Column(Integer, ForeignKey(ChuyenBay.Id), nullable=False)

class HangVe(db.Model):
    __tablename__ = 'HANGVE'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    TenHangVe = Column(String(50), nullable=False)
    IdVeChuyenBay = Column(Integer, ForeignKey(VeChuyenBay.Id), nullable=False)

class PhieuDatCho(db.Model):
    __tablename__ = 'PHIEUDATCHO'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    NgayDat = Column(Date, default=datetime.now(), nullable=False)
    SoGhe = Column(String(10), nullable=False)
    IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
    IdChuyenBay = Column(Integer, ForeignKey(ChuyenBay.Id), nullable=False)
    IdHangVe = Column(Integer, ForeignKey(HangVe.Id), nullable=False)

class VeChuyenBayKhachHang(db.Model):
    __tablename__ = 'VECHUYENBAY_KHACHHANG'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdVeChuyenBay = Column(Integer, ForeignKey(VeChuyenBay.Id), nullable=False)
    IdKhachHang = Column(Integer, ForeignKey(KhachHang.CMND), nullable=False)
    Description = Column(String(100), nullable=True)


if __name__ == '__main__':
    db.create_all()
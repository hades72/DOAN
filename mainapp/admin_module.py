from mainapp import admin, db
from mainapp.model import SanBay, TuyenBay, NhanVien, KhachHang, DonGia, ChuyenBay, MayBay, HoaDon, VeChuyenBay, HangVe, PhieuDatCho, VeChuyenBayKhachHang
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(SanBay, db.session))
admin.add_view(ModelView(TuyenBay, db.session))
admin.add_view(ModelView(NhanVien, db.session))
admin.add_view(ModelView(KhachHang, db.session))
admin.add_view(ModelView(DonGia, db.session))
admin.add_view(ModelView(ChuyenBay, db.session))
admin.add_view(ModelView(MayBay, db.session))
admin.add_view(ModelView(HoaDon, db.session))
admin.add_view(ModelView(VeChuyenBay, db.session))
admin.add_view(ModelView(HangVe, db.session))
admin.add_view(ModelView(PhieuDatCho, db.session))
admin.add_view(ModelView(VeChuyenBayKhachHang, db.session))
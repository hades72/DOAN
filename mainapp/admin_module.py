from mainapp import admin, db
from mainapp.model import Role, Airport, Plane, TicketType, Flight, FlightRoute, User, Plane_TicketType, Intermediarie_AirPort
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Airport, db.session, name = "Sân Bay"))
admin.add_view(ModelView(Plane, db.session, name = "Máy Bay" ))
admin.add_view(ModelView(TicketType, db.session, name = "Hạng Vé"))
admin.add_view(ModelView(Plane_TicketType, db.session, name="Chi tiết máy bay"))
admin.add_view(ModelView(FlightRoute, db.session, name = "Tuyến Bay"))
admin.add_view(ModelView(Flight, db.session, name = "Chuyến Bay"))
admin.add_view(ModelView(Intermediarie_AirPort, db.session, name = "Sân bay trung gian"))
admin.add_view(ModelView(User, db.session, name = "Nhân Viên"))

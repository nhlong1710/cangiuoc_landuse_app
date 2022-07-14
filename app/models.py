from app import db
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
# from flask_login import current_user, login_user, logout_user, login_required
from geoalchemy2 import Geometry


class User(UserMixin, db.Model):
    __tablename__ = "system_user"
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Integer, default=0)

    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Current_Parcel(db.Model):
    __tablename__ = "current_parcel"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String)
    address = db.Column(db.String)
    ward = db.Column(db.String)
    district = db.Column(db.String, default='Cần Giuộc')
    city = db.Column(db.String, default='Long An')
    area = db.Column(db.Float)
    land_use = db.Column(db.String, default='Đất ở')
    updated_year = db.Column(db.Integer, onupdate=date.today().year, default=date.today().year)
    # updated_user = db.Column(db.String)
    geom = db.Column(Geometry('POLYGON'))


class Landuse_History_Record(db.Model):
    __tablename__ = "landuse_history_record"
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey("current_parcel.id"), nullable=False)
    land_use = db.Column(db.String)
    updated_year = db.Column(db.Integer, default=date.today().year)
    # updated_user = db.Column(db.String)


class Ward(db.Model):
    __tablename__ = "ward"
    id = db.Column(db.Integer, primary_key=True)
    ward_name = db.Column(db.String)
    note = db.Column(db.String, default="")


class Land_use(db.Model):
    __tablename__ = "land_use"
    id = db.Column(db.Integer, primary_key=True)
    land_use = db.Column(db.String)
    note = db.Column(db.String, default="")

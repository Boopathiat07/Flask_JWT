from factory import create_app
from geoalchemy2 import Geometry

db = create_app.db
class master(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(30), primary_key = True)
    name = db.Column(db.String(30))
    mobile = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(100))
    
    def __init__(self, email, mobile, password, name):
        self.email = email
        self.mobile = mobile
        self.password = password
        self.name = name

class slave(db.Model):
    __bind_key__ = 'slave'
    
    __tablename__ = 'users'
    email = db.Column(db.String(30), primary_key = True)
    name = db.Column(db.String(30))
    mobile = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(100))
    
    def __init__(self, email, mobile, password, name):
        self.email = email
        self.mobile = mobile
        self.password = password
        self.name = name

class user_session(db.Model):
    jti = db.Column(db.String(50), primary_key = True)
    logIn = db.Column(db.DateTime)
    logout = db.Column(db.DateTime)
    user_id = db.Column(db.String(50))
    islogout = db.Column(db.Boolean , default = False)

    def __init__(self, jti, logIn, logout, user_id, islogout):
        self.jti = jti
        self.logIn = logIn
        self.logout = logout
        self.user_id = user_id
        self.islogout = islogout


class Polygon_table(db.Model):
    __bind_key__ = 'spatial_db'
    __tablename__ = 'polygon_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    geom = db.Column(Geometry('POLYGON', srid=4326))
    
    def __init__(self, id, name, geom):
        self.id = id
        self.name = name
        self.geom = geom


class Restaurant(db.Model):
    __bind_key__ = 'spatial_db'
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    location = db.Column(Geometry('POINT'), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, id, name, distance, location, address):
        self.id = id
        self.name = name
        self.distance = distance
        self.location = location
        self.address = address

        



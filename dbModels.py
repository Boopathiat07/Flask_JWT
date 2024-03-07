from createapp import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __init__(self,id,name,email,date_joined):
        self.name = name
        self.email = email
        self.date_joined = date_joined
        self.id = id
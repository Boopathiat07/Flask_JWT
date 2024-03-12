from create_app import db

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


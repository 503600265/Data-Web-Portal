from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(50))
    first = db.Column(db.String(50))
    last = db.Column(db.String(50))
    
    def __repr__(self):
        return '<Users {}>'.format(self.username)


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    task = db.Column(db.String(80), index=True, unique=False)
    inloc = db.Column(db.String(120), unique=False)
    outloc = db.Column(db.String(120), unique=False)
    start_time = db.Column(db.String(30), unique=False)
    duration = db.Column(db.Float, unique=False)
    inloc_size = db.Column(db.Integer, unique = False)

    def __repr__(self):
        return '<Jobs {}>'.format(self.user_id)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), db.ForeignKey('users.id'))
    time_in = db.Column(db.Integer)
    time_out = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Activity {}>'.format(self.user_id)


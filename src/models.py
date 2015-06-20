from .app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    access_token = db.Column(db.String(120))
    refresh_token = db.Column(db.String(120))
    expires = db.Column(db.Datetime())
    moves_user_id = db.Column(db.Integer())

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

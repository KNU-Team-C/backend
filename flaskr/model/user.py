from flaskr.database import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    is_staff = db.Column(db.Boolean)
    date_joined = db.Column(db.DateTime(timezone = True))



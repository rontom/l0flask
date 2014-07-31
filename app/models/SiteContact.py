from app import db
import datetime


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref='contactauthor')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

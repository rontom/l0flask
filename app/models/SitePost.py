from app import db
import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref='postauthor')
    name = db.Column(db.String(140), index=True, unique=False)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    clndr_datetime = db.Column(db.BigInteger, index=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<Post %r>' % self.body

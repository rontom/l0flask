from app import db
import datetime

STATE_ACTIVE = 1
STATE_DISABLED = 0


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.SmallInteger, default=STATE_ACTIVE)
    name = db.Column(db.String(140), index=True, unique=False, default='anon')
    description = db.Column(db.String(1000), index=True, unique=False, default='anon')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self):
        pass

    def __repr__(self):
        return '<Post %r>' % self.body


ROLE_USER = 0
ROLE_ADMIN = 1


class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_role = db.Column(db.SmallInteger, default=ROLE_USER)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self):
        pass

    def __repr__(self):
        return '<Post %r>' % self.body
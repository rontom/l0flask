import uuid
from werkzeug import generate_password_hash, check_password_hash
from app import db
import datetime
from config import ADMINS

ROLE_USER = 0
ROLE_ADMIN = 1
STATE_ACTIVE = 1
STATE_DISABLED = 0


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), index=True, unique=True)
    pwdhash = db.Column(db.String(254))
    display_name = db.Column(db.String(140), index=True, unique=False, default='anon')
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    state = db.Column(db.SmallInteger, default=STATE_ACTIVE)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, email, password):
        self.email = email.lower()
        self.set_password(password)

    def __str__(self):
        return str(self.id) + ' ' + str(self.email) + ' ' + str(self.display_name)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        if password and self.pwdhash:
            return check_password_hash(self.pwdhash, password)
        else:
            return False

    # make a UUID based on the host ID and current time
    @staticmethod
    def generate_uuid():
        return uuid.uuid1()

    # true if the current user is in the admins list
    def is_admin(self):
        admin = self.email in ADMINS
        if admin:
            return True
        else:
            return False

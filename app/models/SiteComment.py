from app import db
import datetime
import User
import SiteVote
from app import app, db
from ..momentjs import momentjs


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref='commentauthor')
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    votes = db.relationship("Vote", backref='votes')

    def __init__(self):
        pass

    def __repr__(self):
        return '<Comment %r>' % self.body

    def validate(self):
        if len(self.body) <= 0:
            return False
        else:
            return True

    def upvotes(self):
        up = 0
        for v in self.votes:
            if v.vote == 1:
                up += 1
        return str(up)

    def downvotes(self):
        down = 0
        for v in self.votes:
            if v.vote == -1:
                down += 1
        return str(down)
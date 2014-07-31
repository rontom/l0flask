from app import db
import datetime

UPVOTE = 1
DOWNVOTE = -1


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    vote = db.Column(db.Integer, default=UPVOTE)

    def __init__(self):
        pass

    def __repr__(self):
        return '<id %r>' % self.id

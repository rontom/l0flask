from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from app import app, db
from models.User import User
from models.SiteComment import Comment
from models.SiteVote import Vote
from models.SitePost import Post
from models.SiteGroup import Group, GroupMembership
from models.SiteContact import Contact
from forms import RegisterForm, LoginForm, ProfileForm, SubmitForm, ForgotForm
from forms import PasswordForm, GroupForm, PostForm, ContactForm
from forms import AdminForm
from mail import mail
from crypto import crypto
from config import SITE_DOMAIN
from sqlalchemy import desc, asc
import datetime
import time
import calendar


def get_user():
    u = None
    if 'email' in session:
        u = User.query.filter_by(email=session['email'].lower()).first()
    return u


# ####################################################################
# views
#####################################################################

# main page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=get_user())


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form, user=get_user())
        else:
            session['email'] = form.email.data
            return redirect(url_for('index'))
    else:
        return render_template("login.html", form=form, user=get_user())


# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('register.html', form=form, user=get_user())
        else:
            new_user = User(form.email.data, form.password.data)
            new_user.timestamp = datetime.datetime.utcnow()
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
            return redirect(url_for('index'))
    else:
        return render_template('register.html', form=form, user=get_user())


# logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


# forgot
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    session.pop('email', None)
    form = ForgotForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('forgot.html', form=form, user=get_user())
        else:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            m = mail.mail()
            e = crypto.crypto()
            # get encrypted link
            encrypted = e.encrypt(user.id, True)
            # email link
            result = m.send_forgot_password(user.email, encrypted)
            form.email.errors.append(result)
            return render_template('forgot.html', form=form, user=get_user())
    else:
        return render_template('forgot.html', form=form, user=get_user())


# password reset
@app.route('/passwordreset', methods=['GET', 'POST'])
@app.route('/passwordreset/<payload>', methods=['GET', 'POST'])
def password_reset(payload=None):
    form = PasswordForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('passwordreset.html', form=form, user=get_user(), msg=None)
        else:
            # update password
            reset_id = form.reset_id.data
            user = User.query.get(reset_id)
            if user:
                user.set_password(form.password.data)
                db.session.commit()
                msg = "password has been changed. please login again."
            else:
                msg = "user not found."
            return render_template('passwordreset.html', form=form, user=get_user(), msg=msg)
    else:
        e = crypto.crypto()
        decrypted = e.decrypt(payload, True)
        p = User.query.get(decrypted)
        if p:
            return render_template('passwordreset.html', form=form, user=p, msg=None)
        else:
            return render_template('passwordreset.html', form=form, user=get_user(), msg=decrypted)


# profile
@app.route('/u', methods=['GET', 'POST'])
@app.route('/u/<profile_id>', methods=['GET', 'POST'])
def profile(profile_id=None):
    msg = ''
    p = get_user()
    if profile_id:
        p = User.query.get(profile_id)
    form = ProfileForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('profile.html', user=get_user(), profile=p, form=form, msg=msg)
        else:
            u = get_user()
            u.display_name = form.display_name.data
            u.email = form.email.data
            db.session.commit()
            msg = "profile upadted!"
    return render_template('profile.html', user=get_user(), profile=p, form=form, msg=msg)


# groups
@app.route('/g', methods=['GET', 'POST'])
@app.route('/g/<int:id>', methods=['GET', 'POST'])
def groups(group_id=None):
    form = GroupForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            pass
        else:
            pass
    return render_template('groups.html', user=get_user(), form=form)


# submit
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('submit.html', form=form, user=get_user())
        else:
            # save new post
            u = get_user()
            p = Post()
            p.name = form.post_name.data
            p.body = form.post_body.data
            p.clndr_datetime = form.clndr_datetime.data
            p.user_id = u.id
            p.timestamp = datetime.datetime.utcnow()
            db.session.add(p)
            db.session.commit()
            msg = "post successfully added."
            return render_template('submit.html', form=form, user=u, msg=msg, post=p)
    else:
        return render_template('submit.html', form=form, user=get_user())


# post
@app.route('/p/<post_id>')
def post(post_id=None, order=None):
    form = PostForm()
    p = Post.query.get(post_id)
    if p:
        u = User.query.get(p.user_id)
        c = Comment.query.filter_by(post_id=p.id)
    else:
        u = None
        c = None
    return render_template('post.html', user=get_user(), form=form, post=p, author=u, comments=c)


# contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    msg = None
    if request.method == 'POST':
        if not form.validate():
            msg = "not valid."
            return render_template('contact.html', form=form, msg=msg, user=get_user())
        else:
            u = get_user()
            c = Contact()
            c.message = form.cmessage.data
            c.user_id = u.id
            c.timestamp = datetime.datetime.utcnow()
            db.session.add(c)
            db.session.commit()
            msg = "your message has been sent!"
            return render_template('contact.html', form=form, msg=msg, user=u)
    return render_template('contact.html', form=form, msg=msg, user=get_user())


#####################################################################
# static views
#####################################################################

@app.route('/about')
def about():
    return render_template('about.html', user=get_user())


@app.route('/legal')
def legal():
    return render_template('legal.html', user=get_user())


#####################################################################
# admin views
#####################################################################
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm(request.form)
    u = get_user()
    if u.is_admin():
        if request.method == 'POST':
            if not form.validate():
                return render_template('admin/admin.html', form=form, user=get_user())
            else:
                return render_template('admin/admin.html', form=form, user=get_user())
        else:
            return render_template("admin/admin.html", form=form, user=get_user())
    else:
        return redirect(url_for('index'))


#####################################################################
# ajax views
#####################################################################

# posts
@app.route('/ajax/p', methods=["GET"])
def ajax_posts():
    date_time = request.args.get('date_time')
    posts = Post.query.filter_by(clndr_datetime=date_time).order_by(desc(Post.id)).limit(10)
    return render_template('partial/posts.html', posts=posts)


# latest posts
@app.route('/ajax/p/latest', methods=["GET"])
def ajax_posts_latest():
    posts = Post.query.order_by(desc(Post.id)).limit(5)
    return render_template('partial/posts_latest.html', posts=posts)


# comments
@app.route('/ajax/c', methods=["GET"])
def ajax_comments():
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    comments = Comment.query.filter_by(post_id=request.args.get('post_id')).order_by(desc(Comment.timestamp))
    return render_template('partial/comments.html', comments=comments, user=get_user())


# vote
@app.route('/ajax/c/vote', methods=["GET", "POST"])
def ajax_comment_vote():
    u = get_user()
    if u:
        post_id = request.args.get('post_id')
        comment_id = request.args.get('comment_id')
        direction = request.args.get('direction')
        if id and direction:
            # check for existing vote
            old_vote = Vote.query.filter_by(user_id=u.id, comment_id=comment_id).first()
            if old_vote:
                if old_vote.vote != direction:
                    old_vote.vote = direction
                    old_vote.timestamp = datetime.datetime.utcnow()
                    db.session.add(old_vote)
                    db.session.commit()
                return str(old_vote.id)
            v = Vote()
            v.user_id = u.id
            v.post_id = post_id
            v.comment_id = comment_id
            v.vote = direction
            v.timestamp = datetime.datetime.utcnow()
            db.session.add(v)
            db.session.commit()
            return str(v.id)
        else:
            return "error"
    else:
        return 'error : user not authenticated.'


#####################################################################
# json views
#####################################################################

@app.route('/json/p/upcoming', methods=["PUT", "POST"])
def json_post_upcoming():
    data = request.get_json(force=True)
    date_time = data["date_time"]
    posts = Post.query.filter(Post.clndr_datetime > date_time).order_by(desc(Post.clndr_datetime)).limit(5)
    data = []
    for p in posts:
        u = User.query.get(p.user_id)
        data.append({'id': p.id, 'name': p.name, 'body': p.body, 'user': p.user_id, 'username': u.display_name,
                     'date_time': p.clndr_datetime, 'timestamp': p.timestamp})
    return jsonify(posts=data)


# user
@app.route('/json/u', methods=["PUT", "POST"])
def json_user_display_name():
    data = request.get_json(force=True)
    user_id = data["user_id"]
    u = User.query.get(user_id)
    data = []
    if u:
        data.append({'name': u.display_name})
    return jsonify(names=data)


# comment
@app.route('/json/c/submit', methods=["PUT", "POST"])
def json_comment_submit():
    u = get_user()
    if u:
        data = request.get_json(force=True)
        c = Comment()
        c.body = data["comment"]
        c.post_id = data["post_id"]
        c.parent_id = data["parent_id"]
        c.user_id = u.id
        c.user_display_name = u.display_name
        c.timestamp = datetime.datetime.utcnow()
        data = []
        if c.validate():
            db.session.add(c)
            db.session.commit()
            data.append({'commentid': c.id})
            # add vote
            v = Vote()
            v.user_id = u.id
            v.post_id = c.post_id
            v.comment_id = c.id
            v.vote = 1
            v.timestamp = datetime.datetime.utcnow()
            db.session.add(v)
            db.session.commit()
        else:
            data.append({'error': 'no data.'})
    else:
        data = [{'error': 'user not authenticated.'}]

    return jsonify(result=data)

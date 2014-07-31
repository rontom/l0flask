from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, validators, TextAreaField, PasswordField, BooleanField, HiddenField
from models.User import User
from models.SiteComment import Comment

# register
class RegisterForm(Form): 
    email = TextField("email",  [validators.Required("Please enter your email address."), validators.Email("Please enter an email address.")])
    password = PasswordField('password', [validators.Required("Please enter a password.")])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken.")
            return False
        else:
            return True

# login
class LoginForm(Form): 
    email = TextField("email",  [validators.Required("Please enter your email address."), validators.Email("Please enter an email address.")])
    password = PasswordField('password', [validators.Required("Please enter a password.")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Bad Login.")
            return False

# forgot password                
class ForgotForm(Form): 
    email = TextField("email",  [validators.Required("Invalid email address."), validators.Email("Invalid email address.")])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            return True
        else:
            self.email.errors.append("Invalid email address.")
            return False

# password reset            
class PasswordForm(Form): 
    password = PasswordField('password', [validators.Required("Please enter a password.")])
    reset_id = HiddenField("reset_id")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
            
        if len(self.password.data) > 0:
            return True
        else:
            self.password.errors.append("enter a password.")
            return False

# profile
class ProfileForm(Form): 
    display_name = TextField("display_name",  [validators.Required("Please enter a display name.")])
    email = TextField("email",  [validators.Required("Invalid email address."), validators.Email("Invalid email address.")])
    user_id = HiddenField("user_id")
    password = PasswordField('password', [validators.Required("Please enter a password.")])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            u = User.query.get(self.user_id.data)
            email_already_exists = False
            user_with_address = User.query.filter_by(email = self.email.data.lower()).first()
            if user_with_address != None:
                if str(user_with_address.id) != str(self.user_id.data):
                    print(str(user_with_address.id) + " != " + str(self.user_id.data))
                    email_already_exists = True
                
            if len(self.display_name.data) > 50:
                self.display_name.errors.append("max length is 50 characters.")
                return False
            elif email_already_exists:
                self.email.errors.append("email already exists.")
                return False
            else:
                #check password when email has changes
                if u .email != self.email.data:
                    if u.check_password(self.password.data):
                        self.password.errors.append("password must be supplied to update email.")
                        return False
                    else:
                        return True
                else:
                    return True

# groups                
class GroupForm(Form): 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True

# post            
class PostForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True

# submit                
class SubmitForm(Form): 
    post_name = TextField("post_name",  [validators.Required("Please enter a name.")])
    post_body = TextAreaField("post_body",  [validators.Required("Please enter a body.")])
    clndr_datetime = HiddenField("clndr_datetime")
    
    max_name_length = 140
    max_body_length = 1000
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            if len(self.post_name.data) <= 0 or len(self.post_name.data) > self.max_name_length:
                self.post_name.errors.append("name must be less than " + str(self.max_name_length) + " characters.")
                return False
            elif len(self.post_body.data) <= 0 or len(self.post_body.data) > self.max_body_length:
                self.post_body.errors.append("body must be less than " + str(self.max_body_length) + " characters.")
                return False
            elif len(self.clndr_datetime.data) <= 0:
                self.clndr_datetime.errors.append("date time validation failed.")                
                return False            
            else:
                return True

# admin
class AdminForm(Form): 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True

# contact
class ContactForm(Form): 
    cmessage = TextAreaField("cmessage",  [validators.Required("Please enter a message.")])
    
    max_message_length = 1000
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            if len(self.cmessage.data) <= 0 or len(self.cmessage.data) > self.max_message_length:
                error = "message must be less than " + str(self.max_message_length) + " characters."
                self.cmessage.errors.append(error)
                return False   
            else:
                return True

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SITE_DOMAIN = 'domain.com'
CSRF_ENABLED = True
SECRET_KEY = 'secret'

# administrator list
ADMINS = ['test@test.com', 'email@domail.com']

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

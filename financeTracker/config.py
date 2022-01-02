import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECREY_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'data.sqlite')
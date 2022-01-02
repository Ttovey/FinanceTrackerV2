from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/create_account')
def create_account():
    pass

@user.route('/login')
def login():
    pass

@user.route('/logout')
def logout():
    pass
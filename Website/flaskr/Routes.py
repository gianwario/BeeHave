from flask import render_template, Blueprint
from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/loginpage')
def login():
    return render_template('login.html')

from flask import render_template, Blueprint
from flask import Blueprint

views = Blueprint('views', 'views')


@views.route('/')
@views.route('/home')
def homepage():
    return render_template('home.html')


@views.route('/loginpage')
def login():
    return render_template('login.html')

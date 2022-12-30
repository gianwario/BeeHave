from flask import render_template, Blueprint
from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/login_apicoltore')
def login_apicoltore():
    return render_template('login_apicoltore.html')


@views.route('/login_cliente')
def login_cliente():
    return render_template('login_cliente.html')

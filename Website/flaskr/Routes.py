from flask import render_template, Blueprint

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')


@views.route('/registrazione_cl')
def signup_cl():
    return render_template('registrazione_cliente.html')

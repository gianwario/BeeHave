from flask import render_template, Blueprint
from flask_login import login_required

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')


@views.route('/registrazione_apicoltore')
def sigup_ap():
    return render_template('registrazione_apicoltore.html')
@views.route('/areapersonale')
@login_required
def area_personale():

    return render_template('areapersonale.html')
from flask import Blueprint, request, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

from Website.flaskr.Routes import home
from Website.flaskr.gestione_utente.GestioneUtenteService import getApicoltoreByEmail, getClienteByEmail
from Website.flaskr.model.Apicoltore import Apicoltore

gu = Blueprint('gu', __name__)


@gu.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        apicoltore = request.form.get('utente')
        email = request.form.get('email')
        pwd = request.form.get('password')
        if apicoltore:
            user = getApicoltoreByEmail(email)
        else:
            user = getClienteByEmail(email)
        if user and user.password == pwd:
            login_user(user, remember=True)
            session['email']=user.email
        else:
            print("Login non riuscito")
    return home()


@gu.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return home()

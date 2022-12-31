from flask import Blueprint, request, session, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from Website.flaskr.Routes import home, loginpage
from Website.flaskr.gestione_utente.GestioneUtenteService import getApicoltoreByEmail, getClienteByEmail

gu = Blueprint('gu', __name__)


@gu.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = getApicoltoreByEmail(email)
        if user:
            session['isApicoltore'] = True
        else:
            user = getClienteByEmail(email)
            if user:
                session['isApicoltore'] = False
            else:
                return loginpage()
        if user:
            #if check_password_hash(user.password, pwd):
            if user.password == pwd:
                login_user(user, remember=True)
                flash('Login effettuato con successo!', category='success')
                return home()
            else:
                flash('Password errata!', category='error')
        else:
            flash('Email inesistente!', category='error')
    return loginpage()


@gu.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return home()



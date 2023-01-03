import re

from flask import Blueprint, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

from Website.flaskr.Routes import home, login_page
from Website.flaskr.gestione_utente.GestioneUtenteService import *
from Website.flaskr.model.Apicoltore import Apicoltore

gu = Blueprint('gu', __name__)
spec = "[@_!#$%^&*()<>?/'|}{~:]"
num = "0123456789"

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
                return login_page()
        if user:
            if check_password_hash(user.password, pwd):
                login_user(user, remember=True)
                flash('Login effettuato con successo!', category='success')
                return home()
            else:
                flash('Password errata!', category='error')
        else:
            flash('Email inesistente!', category='error')
    return login_page()


@gu.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return home()


@gu.route('/registrazione_ap', methods=['GET', 'POST'])
def sigup():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        indirizzo = request.form.get('indirizzo')
        citta = request.form.get('citta')
        cap = request.form.get('cap')
        telefono = request.form.get('telefono')
        descrizione = request.form.get('descrizione')
        assistenza = bool(request.form.get('assistenza'))
        email = request.form.get('email')
        pwd = request.form.get('password')
        cpwd = request.form.get('cpwd')

        if not 0 < nome.__len__() < 45:
            print("Nome length has to be at last 30 characters", "error")
            return  # inserire pagine html di errore
        if not 0 < cognome.__len__() < 45:
            print("Cognome length has to be at last 30 characters", "error")
            return  # inserire pagine html di errore

        if not 0 < indirizzo.__len__() < 45:
            print("Indirizzo length has to be at last 30 characters ", "error")
            return  # inserire pagine html di errore
        if not 0 < citta.__len__() < 200:
            print("Città length has to be at last 30 characters", "error")
            return  # inserire pagine html di errore
        if not cap.__len__() >= 5:
            print("cap length has to be at last 5 numbers", "error")
            return  # inserire pagine html di errore
        if not 0 < telefono.__len__() < 11:
            print("Telefono length has to be at last 9 numbers", "error")
            return  # inserire pagine html di errore
        if not 0 < descrizione.__len__() < 200:
            print("Descrizione length has to be at last 200 characters", "error")
            return  # inserire pagine html di errore
        if not re.fullmatch('^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,10}$', email):
            print("Invalid email", "error")
            return  # inserire pagine html di errore
        if not pwd.__len__() < 9:
            print("Password length has to be at least 8 characters", "error")
            return  # inserire pagine html di errore

        if not controllo_pwd(pwd):
            print("Password length has to be at least 8 characters", "error")
            return  # inserire pagine html di errore

        if pwd != cpwd:
            print("Password and confirm password do not match", "error")
            return  # inserire pagine html di errore

        user = Apicoltore(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap, telefono=telefono,
                          descrizione=descrizione, email=email, assistenza=assistenza,
                          password=generate_password_hash(pwd, method='sha256'))
        print(user.__dict__)
        registraApicoltore(user)
        return home()

def controllo_pwd(pwd):
    spec_check = re.compile(spec)
    num_check = re.compile(num)

    if (spec_check.search(pwd) is None) and (num_check.search(pwd) is None):
        return True
    else:
        return False

        

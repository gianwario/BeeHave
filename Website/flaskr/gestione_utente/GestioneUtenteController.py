import re
from flask import Blueprint, request, session, flash, redirect, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

from Website.flaskr.Routes import home, loginpage
from Website.flaskr.gestione_utente.GestioneUtenteService import *
from Website.flaskr.model.Cliente import Cliente

gu = Blueprint('gu', __name__)
email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = "[@_!#$%^&*()<>?/'|}{~:]\""
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
                return loginpage()
        if user:
            # if check_password_hash(user.password, pwd):
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


@gu.route('/registrazione_cl', methods=['GET', 'POST'])
def registrazione_cliente():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        psw = request.form.get('psw')
        ripeti_psw = request.form.get('psw-ripeti')
        citta = request.form.get('citta')
        cap = request.form.get('cap')
        indirizzo = request.form.get('indirizzo')
        numtelefono = request.form.get('numtelefono')

        if not re.fullmatch(email_valida, email):
            flash("Il campo e-mail non è nel formato corretto.", category="errore")
        elif psw < 8:
            flash("La password deve contenere almeno 8 caratteri.", category="errore")
        elif not check_email_esistente(email):
            flash("L'indirizzo e-mail è già registrato.", category="errore")
        elif psw != ripeti_psw:
            flash("Ripeti_password non coincide con password.", category="errore")

        elif not controllo_psw(psw):
            flash("Inserire nel campo password almeno un carattere speciale ed un numero.", category="errore")

        else:
            nuovo_cliente = Cliente(email=email, nome=nome, cognome=cognome,
                                    password=generate_password_hash(psw, method='sha256'), indirizzo=indirizzo,
                                    citta=citta, cap=cap, telefono=numtelefono)

        registra_cliente(nuovo_cliente)

        flash("Account creato con successo!", category="successo")
        return redirect("home.html", )

    return render_template("registrazione_cliente.html")


def controllo_psw(psw):
    spec_check = re.compile(spec)
    num_check = re.compile(num)

    if (spec_check.search(psw) is None) and (num_check.search(psw) is None):
        return True
    else:
        return False

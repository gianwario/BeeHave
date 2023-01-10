import re

from flask import Blueprint, request, session, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from Website.flaskr.Routes import home, area_personale, modifica_dati_pers, modifica_psw, login_page, \
    registrazione_apicoltore_page
from Website.flaskr.gestione_utente.GestioneUtenteService import *
from Website.flaskr.model.Apicoltore import Apicoltore

gu = Blueprint('gu', __name__)
email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]
numb = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


@gu.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = get_apicoltore_by_email(email)
        if user:
            session['isApicoltore'] = True

        else:
            user = get_cliente_by_email(email)
            if user:
                session['isApicoltore'] = False
        if user:

            if check_password_hash(user.password, pwd):

                login_user(user)
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

        if not (controllo_car_spec(psw) and controllo_num(psw)):
            flash("Inserire nel campo password almeno un carattere speciale ed un numero.", category="error")
        elif not re.fullmatch(email_valida, email):
            flash("Il campo e-mail non è nel formato corretto.", category="error")
        elif len(psw) < 8:
            flash("La password deve contenere almeno 8 caratteri.", category="error")
        elif not check_email_esistente(email):
            flash("L'indirizzo e-mail è già registrato.", category="error")
        elif psw != ripeti_psw:
            flash("Ripeti_password non coincide con password.", category="error")

        else:
            nuovo_cliente = Cliente(email=email, nome=nome, cognome=cognome,
                                    password=generate_password_hash(psw, method='sha256'),
                                    indirizzo=indirizzo, citta=citta, cap=cap, telefono=numtelefono)

            registra_cliente(nuovo_cliente)
            flash("Account creato con successo!", category="successo")
            return home()

    return sigup_cl()


@gu.route('/registrazione_ap', methods=['GET', 'POST'])
def registra_apicoltore():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        indirizzo = request.form.get('indirizzo')
        citta = request.form.get('citta')
        cap = request.form.get('cap')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        pwd = request.form.get('password')
        cpwd = request.form.get('cpwd')

        if not 0 < len(nome) < 45:
            flash("Nome non valido", category="error")
            return  registrazione_apicoltore_page()
        if not 0 < len(cognome) < 45:
            flash("Cognome non valido", category="error")
            return  registrazione_apicoltore_page()

        if not 0 < len(indirizzo) < 45:
            flash("Indirizzo non valido", category="error")
            return  registrazione_apicoltore_page()
        if not 0 < len(citta) < 200:
            flash("Città non valida", category="error")
            return  registrazione_apicoltore_page()
        if not len(cap) >= 5:
            flash("CAP non valido", category="error")
            return  registrazione_apicoltore_page()
        if not 0 < len(telefono) < 11:
            flash("Numero telefono non valido", category="error")
            return  registrazione_apicoltore_page()
        if not check_email_esistente(email):
            flash("Email già esistente", category="error")
            return  registrazione_apicoltore_page()

        if not len(pwd) < 8:
            flash("Lunghezza password deve essere almeno 8 caratteri", category="error")
            return  registrazione_apicoltore_page()

        if not (controllo_car_spec(pwd) and controllo_num(pwd)):
            flash("Inserire nel campo password almeno un carattere speciale ed un numero.", category="error")
            return  registrazione_apicoltore_page()

        if pwd != cpwd:
            flash("Password e Conferma Password non combaciano", category="error")
            return  registrazione_apicoltore_page()

        user = Apicoltore(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap, telefono=telefono,
                           email=email, assistenza=0,
                          password=generate_password_hash(pwd, method='sha256'))

        registra_apicoltore(user)

    return home()


@gu.route('/modifica_dati_personali', methods=['GET', 'POST'])
@login_required
def modifica_dati_personali():
    if request.method == 'POST':
        g.user = current_user.get_id()
        nome = request.form.get('nuovo_nome')
        cognome = request.form.get('nuovo_cognome')
        email = request.form.get('nuova_email')
        numtelefono = request.form.get('nuovo_numtelefono')

        if not nome:
            nome = current_user.nome
        if not cognome:
            cognome = current_user.cognome
        if not check_email_esistente(email):
            flash("Errore, email già esistente.", category="errore")
            return modifica_dati_pers()
        if not email:
            email = current_user.email
        if not re.fullmatch(email_valida, email):
            flash("Errore, email non nel formato corretto.", category="errore")
            return modifica_dati_pers()
        if not numtelefono:
            numtelefono = current_user.telefono

        modifica_profilo_personale(g.user, nome, cognome, email, numtelefono)

        flash("Modifica password avvenuta con successo!", category="successo")
        return area_personale()


@gu.route('/modifica_indirizzo', methods=['GET', 'POST'])
@login_required
def modifica_indirizzo():
    if request.method == 'POST':
        g.user = current_user.get_id()
        citta = request.form.get('nuova_citta')
        cap = request.form.get('nuovo_cap')
        indirizzo = request.form.get('nuova_indirizzo')
        if not citta:
            citta = current_user.citta
        if not cap:
            cap = current_user.cap
        if not indirizzo:
            indirizzo = current_user.indirizzo

        modifica_residenza(g.user, citta, cap, indirizzo)
        flash("Modifica password avvenuta con successo!", category="successo")
        return area_personale()


@gu.route('/modifica_password', methods=['GET', 'POST'])
@login_required
def modifica_password():
    if request.method == 'POST':
        g.user = current_user.get_id()
        psw = request.form.get('nuova_psw')
        ripeti_psw = request.form.get('nuova_ripeti_psw')

        if psw.__len__() < 8:
            flash("La password deve contenere almeno 8 caratteri.", category="errore")
            return modifica_psw()

        if psw != ripeti_psw:
            flash("Ripeti_password non coincide con password.", category="errore")
            return modifica_psw()

        if not (controllo_car_spec(psw) and controllo_num(psw)):
            flash("Inserire nel campo password almeno un carattere speciale ed un numero.", category="errore")
            return modifica_psw()

        psw = generate_password_hash(psw, method='sha256')
        modifica_password_db(g.user, psw)
        flash("Modifica password avvenuta con successo!", category="successo")
        return area_personale()


def controllo_car_spec(psw):
    for char in psw:
        for symbol in spec:
            if char == symbol:
                return True

    return False


def controllo_num(psw):
    for char in psw:
        for num in numb:
            if char == num:
                return True

    return False

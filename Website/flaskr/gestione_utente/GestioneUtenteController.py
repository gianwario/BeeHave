from flask import Blueprint, request, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from Website.flaskr.Routes import home, area_personale, modifica_dati_utente_page, login_page, \
    registrazione_page
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_email, get_cliente_by_email, \
    registra_utente, modifica_profilo_personale

gu = Blueprint('gu', __name__)


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


@gu.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
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
        is_apicoltore = request.form.get('isApicoltore')

        if registra_utente(nome, cognome, indirizzo, citta, cap, telefono, email, pwd, cpwd, is_apicoltore):
            return home()
    return registrazione_page()


@gu.route('/modifica_dati_utente', methods=['GET', 'POST'])
@login_required
def modifica_dati_utente():
    if request.method == 'POST':
        nome = request.form.get('nuovo_nome')
        cognome = request.form.get('nuovo_cognome')
        email = request.form.get('nuova_email')
        telefono = request.form.get('nuovo_numtelefono')
        citta = request.form.get('nuova_citta')
        cap = request.form.get('nuovo_cap')
        indirizzo = request.form.get('nuovo_indirizzo')
        pwd = request.form.get('nuova_psw')
        cpwd = request.form.get('nuova_ripeti_psw')

        if modifica_profilo_personale(nome, cognome, email, telefono, citta, cap, indirizzo, pwd, cpwd):
            return area_personale()

    return modifica_dati_utente_page()

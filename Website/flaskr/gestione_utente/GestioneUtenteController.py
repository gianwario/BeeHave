import os

from flask import Blueprint, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import home, area_personale, modifica_dati_utente_page, login_page, \
    registrazione_page
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_email, get_cliente_by_email, \
    controlla_email_esistente, registra_utente, modifica_profilo_personale, aggiorna_avatar, \
    aggiorna_avatar
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente

gu = Blueprint('gu', __name__)
email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]


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
        is_apicoltore = bool(int(request.form.get('isApicoltore')))

        if controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
            if not controlla_email_esistente(email):
                flash("Email già esistente", category="error")
            elif controlla_password(pwd, cpwd):
                if is_apicoltore:
                    user = Apicoltore(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap,
                                      telefono=telefono,
                                      email=email, assistenza=0, password=generate_password_hash(pwd, method='sha256'))
                else:
                    user = Cliente(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap,
                                   telefono=telefono,
                                   email=email, password=generate_password_hash(pwd, method='sha256'))

                registra_utente(user)
                avatar = 'beekeeper.png'
                nome_avatar_cliente = 'avatar_cliente' + str(user.id) + ".jpg"
                nome_avatar_apicoltore = 'avatar_apicoltore' + str(user.id) + ".jpg"

                try:
                    image = request.files['imagepath']
                    path_image = os.path.join(image_folder_absolute, secure_filename(image.filename))
                    try:
                        image.save(path_image)
                        if is_apicoltore:
                            os.rename(path_image, os.path.join(image_folder_absolute, nome_avatar_apicoltore))
                            aggiorna_avatar(user.id, nome_avatar_apicoltore)
                        else:
                            os.rename(path_image, os.path.join(image_folder_absolute, nome_avatar_cliente))
                            aggiorna_avatar(user.id, nome_avatar_cliente)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                    if is_apicoltore:
                        aggiorna_avatar(user.id, avatar)
                    else:
                        aggiorna_avatar(user.id, avatar)

                session['isApicoltore'] = is_apicoltore
                login_user(user)
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

        nome_avatar_cliente = 'avatar_cliente' + str(current_user.id) + ".jpg"
        nome_avatar_apicoltore = 'avatar_apicoltore' + str(current_user.id) + ".jpg"

        if controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
            if not controlla_email_esistente(email) and email != current_user.email:
                flash("Email già esistente", category="error")
            elif pwd != '':
                # todo Avvisare L'utente che i cambiamenti avvengono solo dopo aver inserito pwd
                if controlla_password(pwd, cpwd):
                    modifica_profilo_personale(nome, cognome, email, telefono, citta, cap, indirizzo, pwd)
                    try:
                        image = request.files['imagepath']
                        path_image = os.path.join(image_folder_absolute, secure_filename(image.filename))
                        try:
                            image.save(path_image)
                            if session['isApicoltore']:
                                os.remove(os.path.join(image_folder_absolute, nome_avatar_apicoltore))
                                os.rename(path_image, os.path.join(image_folder_absolute, nome_avatar_apicoltore))
                                aggiorna_avatar(current_user.id, nome_avatar_apicoltore)
                            else:
                                os.remove(os.path.join(image_folder_absolute, nome_avatar_cliente))
                                os.rename(path_image, os.path.join(image_folder_absolute, nome_avatar_cliente))
                                aggiorna_avatar(current_user.id, nome_avatar_cliente)
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
            return area_personale()
    return modifica_dati_utente_page()


def controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
    if not 0 < len(nome) <= 45:
        flash("Nome non valido", category="error")
    elif not 0 < len(cognome) <= 45:
        flash("Cognome non valido", category="error")
    elif not 0 < len(indirizzo) <= 50:
        flash("Indirizzo non valido", category="error")
    elif not 0 < len(citta) <= 45:
        flash("Città non valida", category="error")
    elif not 0 < len(cap) <= 5 or not cap.isdigit():
        flash("CAP non valido", category="error")
    elif not 0 < len(telefono) <= 10 or not telefono.isdigit():
        flash("Numero telefono non valido", category="error")
    elif not 0 < len(email) <= 45:
        flash("Email non valida", category="error")
    else:
        return True
    return False


def controlla_password(pwd, cpwd):
    if len(pwd) < 8:
        flash("Lunghezza password deve essere almeno 8 caratteri.", category="error")
    elif not (controllo_caratteri_speciali(pwd) and controllo_numeri(pwd)):
        flash("Inserire nel campo password almeno un carattere speciale ed un numero.", category="error")
    elif pwd != cpwd:
        flash("Password e Conferma Password non combaciano.", category="error")
    else:
        return True
    return False


def controllo_caratteri_speciali(psw):
    for char in psw:
        for symbol in spec:
            if char == symbol:
                return True
    return False


def controllo_numeri(psw):
    for char in psw:
        if char.isdigit():
            return True
    return False

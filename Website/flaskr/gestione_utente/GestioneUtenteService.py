from flask import session, flash
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash

from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db

email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]


def get_apicoltore_by_email(email):
    return Apicoltore.query.filter_by(email=email).first()


def get_apicoltore_by_id(id_api):
    return Apicoltore.query.filter_by(id=id_api).first()


def get_cliente_by_id(id_cliente):
    return Cliente.query.filter_by(id=id_cliente).first()


def get_cliente_by_email(email):
    return Cliente.query.filter_by(email=email).first()


def controlla_email_esistente(email):
    if Cliente.query.filter_by(email=email).first() or Apicoltore.query.filter_by(email=email).first():
        return False
    else:
        return True


def registra_utente(nome, cognome, indirizzo, citta, cap, telefono, email, password, conferma_password, is_apicoltore):
    if controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
        if not controlla_email_esistente(email):
            flash("Email già esistente", category="error")
        elif controlla_password(password, conferma_password):
            if is_apicoltore is None or not is_apicoltore.isdigit():
                flash("is_apicoltore non è valido")
            elif int(is_apicoltore):
                user = Apicoltore(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap,
                                  telefono=telefono,
                                  email=email, assistenza=0, password=generate_password_hash(password, method='sha256'))
            else:
                user = Cliente(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap,
                               telefono=telefono,
                               email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            session['isApicoltore'] = is_apicoltore
            login_user(user)
            return True
    return False


def modifica_profilo_personale(nome, cognome, email, telefono, citta, cap, indirizzo, pwd, cpwd):
    if controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
        if not controlla_email_esistente(email) and email != current_user.email:
            flash("Email già esistente", category="error")
            return False
        if pwd != '' and not controlla_password(pwd, cpwd):
            return False
        if session['isApicoltore']:
            utente = get_apicoltore_by_id(current_user.id)
        else:
            utente = get_cliente_by_id(current_user.id)

        current_user.nome = utente.nome = nome
        current_user.cognome = utente.cognome = cognome
        current_user.email = utente.email = email
        current_user.telefono = utente.telefono = telefono
        current_user.citta = utente.citta = citta
        current_user.cap = utente.cap = cap
        current_user.indirizzo = utente.indirizzo = indirizzo
        if pwd != '':
            current_user.password = utente.password = generate_password_hash(pwd, method='sha256')

        db.session.commit()
        return True
    return False


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

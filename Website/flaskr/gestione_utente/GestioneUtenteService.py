from flask import session
from flask_login import current_user
from werkzeug.security import generate_password_hash

from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db


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


def registra_utente(utente):
    db.session.add(utente)
    db.session.commit()


def modifica_profilo_personale(nome, cognome, email, telefono, citta, cap, indirizzo, pwd):
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
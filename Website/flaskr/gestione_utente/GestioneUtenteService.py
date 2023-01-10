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


def check_email_esistente(email):
    if Cliente.query.filter_by(email=email).first():
        return False
    else:
        return True


def registra_cliente(cliente):
    db.session.add(cliente)
    db.session.commit()


def registra_apicoltore(utente):
    db.session.add(utente)
    db.session.commit()


def modifica_profilo_personale(uid, nome, cognome, email, numtelefono):
    cliente = get_cliente_by_id(uid)
    if not cliente:
        apicoltore = get_apicoltore_by_id(uid)
        if not apicoltore:
            print("Errore comunicazione con db")
            return  #
        else:
            apicoltore.nome = nome
            apicoltore.cognome = cognome
            apicoltore.email = email
            apicoltore.telefono = numtelefono
            db.session.commit()
    else:
        cliente.nome = nome
        cliente.cognome = cognome
        cliente.email = email
        cliente.telefono = numtelefono
        db.session.commit()


def modifica_residenza(uid, citta, cap, indirizzo):
    cliente = get_cliente_by_id(uid)
    if not cliente:
        apicoltore = get_apicoltore_by_id(uid)
        if not apicoltore:
            print("Errore comunicazione con db")
            return  #
        else:
            apicoltore.citta = citta
            apicoltore.cap = cap
            apicoltore.indirizzo = indirizzo
            db.session.commit()
    else:
        cliente.citta = citta
        cliente.cap = cap
        cliente.indirizzo = indirizzo
        db.session.commit()


def modifica_password_db(uid, psw):
    cliente = get_cliente_by_id(uid)
    if not cliente:
        apicoltore = get_apicoltore_by_id(uid)
        if not apicoltore:
            print("Errore comunicazione con db")
            return  #
        else:
            apicoltore.password = psw
            db.session.commit()
    else:
        cliente.password = psw
        db.session.commit()

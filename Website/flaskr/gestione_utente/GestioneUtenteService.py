from Website.flaskr import db
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db


def getApicoltoreByEmail(email):
    return Apicoltore.query.filter_by(email=email).first()


def getApicoltoreById(id_api):
    return Apicoltore.query.filter_by(id=id_api).first()


def getClienteByEmail(email):
    return Cliente.query.filter_by(email=email).first()


def check_email_esistente(email):
    if Cliente.query.filter_by(email=email).first():
        return False
    else:
        return True


def registra_cliente(Cliente):
    db.session.add(Cliente)
    db.session.commit()


def registraApicoltore(utente):
    db.session.add(utente)
    db.session.commit()


def modifica_profilo_personale(uid, nome, cognome, email, numtelefono):
    cliente = Cliente.query.filter_by(id=uid).first()
    if not cliente:
        apicoltore = Apicoltore.query.filter_by(id=uid).first()
        if not apicoltore:
            print("Errore comunicazione con db")
            return  ###
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
        print("cl_successo_datiperso")
        db.session.commit()


def modifica_residenza(uid, citta, cap, indirizzo):
    cliente = Cliente.query.filter_by(id=uid).first()
    if not cliente:
        apicoltore = Apicoltore.query.filter_by(id=uid).first()
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
        print("ap_successo_residenz")
        db.session.commit()

from Website.flaskr import db
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db

spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]
numb = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


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

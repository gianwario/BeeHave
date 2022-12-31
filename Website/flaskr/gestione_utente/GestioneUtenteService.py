from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db


def getApicoltoreByEmail(email):
    return Apicoltore.query.filter_by(email=email).first()


def getClienteByEmail(email):
    return Cliente.query.filter_by(email=email).first()

def registraApicoltore(utente):
    db.session.add(utente)
    db.session.commit()
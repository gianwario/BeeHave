from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db


def get_apicoltore_by_email(email):
    return Apicoltore.query.filter_by(email=email).first()


def get_apicoltore_by_id(id_api):
    return Apicoltore.query.filter_by(id=id_api).first()


def get_cliente_by_email(email):
    return Cliente.query.filter_by(email=email).first()


def registra_apicoltore(utente):
    db.session.add(utente)
    db.session.commit()

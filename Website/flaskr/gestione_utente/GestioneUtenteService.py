from Website.flaskr import db
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente


def getApicoltoreByEmail(email):
    return Apicoltore.query.filter_by(email=email).first()


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

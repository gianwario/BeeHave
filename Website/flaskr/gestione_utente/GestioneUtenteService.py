from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente


def getApicoltoreByEmail(email):
    return Apicoltore.query.filter_by(email=email).first()


def getClienteByEmail(email):
    return Cliente.query.filter_by(email=email).first()

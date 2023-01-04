from Website.flaskr import db
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db

spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]
numb = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


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


def controllo_car_spec(psw):
    for char in psw:
        for symbol in spec:
            if char == symbol:
                return True

    return False


def controllo_num(psw):
    for char in psw:
        for num in numb:
            if char == num:
                return True

    return False


def registra_cliente(Cliente):
    db.session.add(Cliente)
    db.session.commit()

def registraApicoltore(utente):
    db.session.add(utente)
    db.session.commit()

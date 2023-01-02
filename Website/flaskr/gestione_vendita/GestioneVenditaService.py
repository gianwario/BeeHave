
from Website.flaskr.model.Prodotto import Prodotto
from .. import db


def getProdottoById(id):
    return Prodotto.query.filter_by(id=id).first()


def getTuttiProdotti():
    return Prodotto.query.all()

def inserisci_prodotto(prodotto):
    db.session.add(prodotto)
    db.session.commit()

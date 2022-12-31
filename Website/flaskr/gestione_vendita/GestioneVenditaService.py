from Website.flaskr.model.Prodotto import Prodotto
from .. import db


def getProdottoById(id):
    return Prodotto.query.filter_by(id=id).first()
def inserisciProdotto(prodotto):
    db.session.add(prodotto)
    db.session.commit()
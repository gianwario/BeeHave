
from Website.flaskr.model.Prodotto import Prodotto
from .. import db


def getProdottoById(id):
    return Prodotto.query.filter_by(id=id).first()


def inserisciProdotto(prodotto):
    db.session.add(prodotto)
    db.session.commit()


def getTuttiProdotti():
    return Prodotto.query.all()

def inserisci_prodotto(nome, descrizione, localita, peso, tipologia, prezzo, quantita, apicoltore):
    prodotto = Prodotto(nome=nome, descrizione=descrizione,
                        localita=localita, peso=peso, tipologia=tipologia, prezzo=prezzo, quantita=quantita, apicoltore=apicoltore)
    db.session.add(prodotto)
    db.session.commit()


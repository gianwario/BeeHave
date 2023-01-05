from Website.flaskr.model.Prodotto import Prodotto
from .. import db


def getProdottoById(id):
    return Prodotto.query.filter_by(id=id).first()


def updateImage(id, image):
    prodotto = getProdottoById(id)
    prodotto.img_path = str(image)
    db.session.flush()
    db.session.commit()


def deleteProdotto(prodotto_id):
    prod = getProdottoById(prodotto_id)
    db.session.delete(prod)
    db.session.commit()


def getTuttiProdotti():
    return Prodotto.query.all()


def inserisci_prodotto(prodotto):
    db.session.add(prodotto)
    db.session.commit()


def decrementa_qnt(id_prodotto, qnt):
    prod = Prodotto.query.filter_by(id=id_prodotto).first()
    prod.quantita -= int(qnt)
    db.session.flush()
    db.session.commit()


def get_ProdottiByApicoltore(apicoltore_id):
    return Prodotto.query.filter_by(id_apicoltore=apicoltore_id).all()


def acquisto_prodotto(acquisto, qnt):
    db.session.add(acquisto)
    db.session.commit()
    decrementa_qnt(acquisto.id_prodotto, qnt)

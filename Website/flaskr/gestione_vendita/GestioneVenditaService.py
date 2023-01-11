from Website.flaskr.model.Prodotto import Prodotto
from .. import db


def get_prodotto_by_id(id):
    return Prodotto.query.filter_by(id=id).first()


def aggiorna_immagine(id, image):
    prodotto = get_prodotto_by_id(id)
    prodotto.img_path = str(image)
    db.session.flush()
    db.session.commit()


def cancella_prodotto(prodotto_id):
    prod = get_prodotto_by_id(prodotto_id)
    db.session.delete(prod)
    db.session.commit()


def get_tutti_prodotti():
    return Prodotto.query.all()


def inserisci_prodotto(prodotto):
    db.session.add(prodotto)
    db.session.commit()


def decrementa_quantita(id_prodotto, qnt):
    prod = Prodotto.query.filter_by(id=id_prodotto).first()
    prod.quantita -= int(qnt)
    db.session.flush()
    db.session.commit()


def get_prodotti_by_apicoltore(apicoltore_id):
    return Prodotto.query.filter_by(id_apicoltore=apicoltore_id).all()


def acquisto_prodotto(acquisto, qnt):
    db.session.add(acquisto)
    db.session.commit()
    decrementa_quantita(acquisto.id_prodotto, qnt)

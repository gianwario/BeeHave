from flask_login import current_user

from Website.flaskr.model.Prodotto import Prodotto
from .. import db


def get_prodotto_by_id(id_prodotto):
    return Prodotto.query.filter_by(id=id_prodotto).first()


def aggiorna_immagine(id_prodotto, image):
    prodotto = get_prodotto_by_id(id_prodotto)
    prodotto.img_path = str(image)
    db.session.flush()
    db.session.commit()


def cancella_prodotto(prodotto_id):
    prodotto = get_prodotto_by_id(prodotto_id)
    prodotto.quantita = 0
    db.session.commit()


def get_tutti_prodotti():
    return Prodotto.query.all()


def inserisci_prodotto(prodotto):
    db.session.add(prodotto)
    db.session.commit()


def decrementa_quantita(id_prodotto, quantita):
    prodotto = Prodotto.query.filter_by(id=id_prodotto).first()
    prodotto.quantita -= int(quantita)
    db.session.flush()
    db.session.commit()


def get_prodotti_by_apicoltore(id_apicoltore):
    return Prodotto.query.filter_by(id_apicoltore=id_apicoltore).all()


def acquisto_prodotto(acquisto, quantita):
    db.session.add(acquisto)
    db.session.commit()
    decrementa_quantita(acquisto.id_prodotto, quantita)

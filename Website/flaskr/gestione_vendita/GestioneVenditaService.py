from flask import flash
from flask_login import current_user

from Website.flaskr.model.Prodotto import Prodotto
from .. import db
from ..model.Acquisto import Acquisto


def get_prodotto_by_id(id_prodotto):
    return Prodotto.query.filter_by(id=id_prodotto).first()


def cancella_prodotto(prodotto_id):
    prodotto = get_prodotto_by_id(prodotto_id)
    prodotto.quantita = 0
    db.session.commit()


def get_tutti_prodotti():
    return Prodotto.query.all()


def inserisci_prodotto(nome, descrizione, localita, peso, tipologia, prezzo, quantita):
    if nome is None or not 0 < len(nome) <= 30:
        flash('Lunghezza nome non valida!', category='error')
    elif descrizione is None or not 0 < len(descrizione) <= 200:
        flash('Lunghezza descrizione non valida!', category='error')
    elif localita is None or not 0 < len(localita) <= 40:
        flash('Lunghezza località non valida!', category='error')
    elif peso is None or not peso.isdigit() or not 0 < int(peso) <= 1000:
        flash('Peso non è nel range corretto', category='error')
    elif tipologia is None or not 0 < len(tipologia) <= 30:
        flash('Lunghezza tipologia non valida!', category='error')
    elif prezzo is None or not 0 < float(prezzo) <= 1000:
        flash('Prezzo non è nel range corretto!', category='error')
    elif quantita is None or not quantita.isdigit() or not 0 < int(quantita) <= 1000000:
        flash('Quantità non è nel range corretto!', category='error')
    else:
        flash('Inserimento avvenuto con successo!', category='success')
        prodotto = Prodotto(nome=nome, descrizione=descrizione, localita=localita, peso=int(peso), prezzo=float(prezzo),
                            quantita=int(quantita), id_apicoltore=current_user.id, tipologia=tipologia)
        db.session.add(prodotto)
        db.session.commit()
        return True
    return False


def decrementa_quantita(id_prodotto, quantita):
    prodotto = Prodotto.query.filter_by(id=id_prodotto).first()
    prodotto.quantita -= int(quantita)
    db.session.flush()
    db.session.commit()


def get_prodotti_by_apicoltore(id_apicoltore):
    return Prodotto.query.filter_by(id_apicoltore=id_apicoltore).all()


def acquisto_prodotto(id_prodotto, quantita):
    if id_prodotto is None or not id_prodotto.isdigit():
        flash('ID Prodotto non valido!', category='error')
    elif quantita is None or not quantita.isdigit() or int(quantita) > get_prodotto_by_id(int(id_prodotto)).quantita:
        flash('Quantitá non disponibile!', category='error')
    else:
        acquisto = Acquisto(id_prodotto=id_prodotto, quantita=quantita)
        db.session.add(acquisto)
        db.session.commit()
        decrementa_quantita(acquisto.id_prodotto, quantita)
        flash('Acquisto andato a buon fine!', category='success')
        return True
    return False

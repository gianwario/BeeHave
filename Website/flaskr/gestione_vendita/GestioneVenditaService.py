from flask import flash

from Website.flaskr.model.Prodotto import Prodotto
from .. import db
from ..model.Acquisto import Acquisto

"""
    Restituisce un prodotto dato l'id
"""


def get_prodotto_by_id(id_prodotto):
    return Prodotto.query.filter_by(id=id_prodotto).first()


"""
    Gestisce la rimozione di un prodotto
    pre: get_prodotto_by_id(prodotto_id) is not None 
    post: get_prodotto_by_id(prodotto_id).quantita==0 
"""


def cancella_prodotto(prodotto_id):
    prodotto = get_prodotto_by_id(prodotto_id)
    if prodotto is None:
        flash("Il prodotto non esiste!", category='error')
    else:
        prodotto.quantita = 0
        db.session.commit()
        flash("Prodotto eliminato con successo!", category='success')
        return True
    return False


"""
    Restituisce tutti i prodotti
"""


def get_tutti_prodotti():
    return Prodotto.query.all()


"""
    Gestisce l'inserimento di un prodotto da parte di un apicoltore
    pre: apicoltore is not None
"""


def inserisci_prodotto(nome, descrizione, localita, peso, tipologia, prezzo, quantita, apicoltore):
    if not isinstance(nome, str) or not 0 < len(nome) <= 30:
        flash('Lunghezza nome non valida!', category='error')
    elif not isinstance(descrizione, str) or not 0 < len(descrizione) <= 200:
        flash('Lunghezza descrizione non valida!', category='error')
    elif not isinstance(localita, str) or not 0 < len(localita) <= 40:
        flash('Lunghezza località non valida!', category='error')
    elif not isinstance(peso, str) or not peso.isdigit() or not 0 < int(peso) <= 1000:
        flash('Peso non è nel range corretto', category='error')
    elif not isinstance(tipologia, str) or not 0 < len(tipologia) <= 30:
        flash('Lunghezza tipologia non valida!', category='error')
    elif not isinstance(prezzo, str) or prezzo == '' or not 0 < float(prezzo) <= 1000:
        flash('Prezzo non è nel range corretto!', category='error')
    elif not isinstance(quantita, str) or not quantita.isdigit() or not 0 < int(quantita) <= 1000000:
        flash('Quantità non è nel range corretto!', category='error')
    else:
        prodotto = Prodotto(nome=nome, descrizione=descrizione, localita=localita, peso=int(peso), prezzo=float(prezzo),
                            quantita=int(quantita), id_apicoltore=apicoltore.id, tipologia=tipologia)
        db.session.add(prodotto)
        db.session.commit()
        flash('Inserimento avvenuto con successo!', category='success')
        return True
    return False


"""
    Decrementa la quantità di un prodotto all'interno del catalogo
    pre: get_prodotto_by_id(prodotto_id).quantita is not None and get_prodotto_by_id(prodotto_id) >= quantita
    post: @pre.get_prodotto_by_id(int(id_prodotto)).quantita==get_prodotto_by_id(int(id_prodotto)).quantita - quantita 
"""


def decrementa_quantita(id_prodotto, quantita):
    prodotto = Prodotto.query.filter_by(id=id_prodotto).first()
    if prodotto is None:
        flash("Il prodotto non esiste!", category='error')
    else:
        prodotto.quantita -= quantita
        db.session.flush()
        db.session.commit()
        return True
    return False


"""
    Restituisce tutti i prodotti di un apicoltore
    pre: get_apicoltore_by_id(id_apicoltore) is not None 
"""


def get_prodotti_by_apicoltore(id_apicoltore):
    return Prodotto.query.filter_by(id_apicoltore=id_apicoltore).all()


"""
    Gestisce l'acquisto di un prodotto da parte di un cliente
    pre: cliente is not None
"""


def acquisto_prodotto(id_prodotto, quantita, cliente):
    if not isinstance(id_prodotto, str) or not id_prodotto.isdigit():
        flash('ID Prodotto non valido!', category='error')
    elif not isinstance(quantita, str) or not quantita.isdigit() or \
            not 0 < int(quantita) <= get_prodotto_by_id(int(id_prodotto)).quantita:
        flash('Quantitá non disponibile!', category='error')
    else:
        acquisto = Acquisto(id_cliente=cliente.id, id_prodotto=int(id_prodotto), quantita=int(quantita))
        db.session.add(acquisto)
        db.session.commit()
        decrementa_quantita(acquisto.id_prodotto, acquisto.quantita)
        flash('Acquisto andato a buon fine!', category='success')
        return True
    return False

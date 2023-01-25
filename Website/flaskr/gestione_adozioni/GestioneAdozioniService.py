import datetime

from flask import flash

from Website.flaskr import db
from Website.flaskr.model.Alveare import Alveare
from Website.flaskr.model.TicketAdozione import TicketAdozione

"""
    Gestisce l'inserimento di un alveare da parte di un apicoltore
    Pre: apicoltore is not None
    Post: get_alveare_by_id(alveare.id) is not None
"""


def inserisci_alveare(nome, produzione, numero_api, tipo_miele, prezzo, tipo_fiore, apicoltore):
    if not isinstance(nome, str) or not 0 < len(nome) <= 30:
        flash('Lunghezza Nome non valida!', category='error')
    elif not isinstance(nome, str) or not 0 < len(tipo_fiore) <= 30:
        flash('Lunghezza di TipoFiore non valida!', category='error')
    elif not isinstance(produzione, str) or not produzione.isdigit() or not 0 < int(produzione) <= 2000:
        flash('Quantità produzione non è nel range corretto!', category='error')
    elif not isinstance(tipo_miele, str) or not 0 < len(tipo_miele) <= 30:
        flash('Lunghezza di TipoMiele non valida!', category='error')
    elif not isinstance(numero_api, str) or not numero_api.isdigit() or not 0 < int(numero_api) <= 40000:
        flash('NumeroApi non è nel range corretto!', category='error')
    elif not isinstance(prezzo, str) or not prezzo.replace('.', '', 1).isdigit() or not 0 < float(prezzo) <= 1000:
        flash('Prezzo non è nel range corretto!', category='error')
    else:
        alveare = Alveare(nome=nome, produzione=int(produzione), numero_api=int(numero_api), tipo_miele=tipo_miele,
                          percentuale_disponibile=100,
                          prezzo=float(prezzo), tipo_fiore=tipo_fiore, id_apicoltore=apicoltore.id)
        flash('Inserimento avvenuto con successo!', category='success')

        db.session.add(alveare)
        db.session.commit()
        return True
    return False


"""
    Restituisce l'alveare dato l'id
"""


def get_alveare_by_id(alveare_id):
    return Alveare.query.filter_by(id=alveare_id).first()


"""
    Restituisce tutti gli alveari
"""


def get_alveari():
    return Alveare.query.all()


"""
    Decrementa la percentuale disponibile dell'alveare
    pre: alveare is not None and alveare.percentuale_disponibile >= percentuale
    post: alveare is not None and @pre.alveare.percentuale_disponibile == .alveare.percentuale_disponibile - percentuale
"""


def decrementa_percentuale(alveare, percentuale):
    alveare.percentuale_disponibile -= int(percentuale)
    db.session.flush()
    db.session.commit()


"""
    Gestisce l'adozione dell'alveare da parte di un cliente
    pre: alveare is not None and cliente is not None
    post: get_ticket_adozione(cliente.id).get(alveare) is not None
"""


def adozione_alveare(alveare, cliente, tempo_adozione, percentuale):
    if not isinstance(tempo_adozione, str) or not tempo_adozione.isdigit() or not 3 <= int(tempo_adozione) <= 12:
        flash('Tempo Adozione non è nel range corretto!', category='error')
    elif not isinstance(percentuale, str) or not percentuale.isdigit() or not 25 <= int(percentuale) <= 100:
        flash('Percentuale Adozione non è nel range corretto!', category='error')
    elif int(percentuale) > alveare.percentuale_disponibile:
        flash('Percentuale Adozione è maggiore di Percentuale Disponibile!', category='error')

    else:
        ticket = TicketAdozione(id_cliente=cliente.id, id_alveare=alveare.id,
                                percentuale_adozione=int(percentuale),
                                data_inizio_adozione=datetime.datetime.now(), tempo_adozione=int(tempo_adozione))
        db.session.add(ticket)
        db.session.commit()
        decrementa_percentuale(alveare, percentuale)
        flash('Alveare adottato con successo!', category='success')
        return True
    return False


"""
    Gestisce l'aggiornamento dello stato dell'alveare da parte di un apicoltore
    pre: alveare is not None
"""


def aggiorna_stato(alveare, covata_compatta, popolazione, polline, stato_cellette, stato_larve):
    if not isinstance(covata_compatta, str) or not covata_compatta.isdigit():
        flash('CovataCompatta non è stata inserita!', category='error')
    elif not isinstance(popolazione, str) or not 0 < len(popolazione) <= 30:
        flash('Lunghezza di Popolazione non valida!', category='error')
    elif not isinstance(polline, str) or not 0 < len(polline) <= 30:
        flash('Lunghezza di Polline non valida!', category='error')
    elif not isinstance(stato_cellette, str) or not 0 < len(stato_cellette) <= 30:
        flash('Lunghezza di Stato Cellette non valida!', category='error')
    elif not isinstance(stato_larve, str) or not 0 < len(stato_larve) <= 30:
        flash('Lunghezza di Stato Larve non valida!', category='error')
    else:
        alveare.covata_compatta = bool(int(covata_compatta))
        alveare.popolazione = popolazione
        alveare.polline = polline
        alveare.stato_cellette = stato_cellette
        alveare.stato_larve = stato_larve
        db.session.flush()
        db.session.commit()
        flash('Stato alveare aggiornato correttamente', category='success')
        return True
    return False


"""
    Restituisce gli alveari di un apicoltore
    pre: get_apicoltore_by_id(apicoltore_id) is not None
"""


def get_alveari_from_apicoltore(apicoltore_id):
    return Alveare.query.filter_by(id_apicoltore=apicoltore_id).all()


"""
    Restituisce gli alveari adottati da un cliente
    pre: get_cliente_by_id(cliente_id) is not None
"""


def get_ticket_adozione(cliente_id):
    return db.session.query(TicketAdozione, Alveare).filter_by(id_cliente=cliente_id).join(Alveare).all()


"""
    Restituisce i ticket di adozione di un alveare
    pre: get_alveare_by_id(id_alveare) is not None
"""


def get_ticket_from_alveare(id_alveare):
    return TicketAdozione.query.filter_by(id_alveare=id_alveare).all()

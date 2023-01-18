import datetime

from flask import flash
from flask_login import current_user

from .. import db
from ..gestione_utente.GestioneUtenteService import get_apicoltore_by_id
from ..model.Apicoltore import Apicoltore
from ..model.TicketAssistenza import TicketAssistenza


def inserisci_area_assistenza(descrizione, apicoltore):
    if not isinstance(descrizione, str) or not 0 < len(descrizione) <= 200:
        flash('La lunghezza della descrizione non è valida!', category='error')
    else:
        apicoltore.descrizione = descrizione
        apicoltore.assistenza = True
        db.session.commit()
        flash('Messa a disposizione area assistenza avvenuta con successo!', category='success')
        return True
    return False


def get_numero_ticket_assistenza_apicoltore(id_apicoltore):
    return len(TicketAssistenza.query.filter_by(id_apicoltore=id_apicoltore).all())


def get_assistenti():
    return Apicoltore.query.filter_by(assistenza=1).all()


# Controllo se l'apicoltore esiste ed è disponibile a fornire assistenza
def controlla_apicoltore(id_apicoltore):
    apicoltore = get_apicoltore_by_id(id_apicoltore)
    if apicoltore:
        return apicoltore.assistenza
    return False


def richiedi_assistenza(nome, descrizione, id_apicoltore, cliente):
    if not isinstance(nome, str) or not 0 < len(nome) <= 45:
        flash('La lunghezza del nome non è valida', category='error')
    elif not isinstance(descrizione, str) or not 0 < len(descrizione) <= 200:
        flash('La lunghezza della descrizione non è valida!', category='error')
    elif not isinstance(id_apicoltore, str) or not id_apicoltore.isdigit() or not controlla_apicoltore(int(id_apicoltore)):
        flash("L'apicoltore non esiste o non è disponibile a fornire assistenza", category='error')
    else:
        ticket = TicketAssistenza(id_cliente=cliente.id, id_apicoltore=int(id_apicoltore), nome=nome,
                                  descrizione=descrizione, data_inizio=datetime.datetime.now(), stato='Creato')
        db.session.add(ticket)
        db.session.commit()
        flash('Richiesta assistenza avvenuta con successo!', category='success')
        return True
    return False


def get_numero_ticket_assistenza_apicoltore(id_apicoltore):
    return len(TicketAssistenza.query.filter_by(id_apicoltore=id_apicoltore).all())


def get_numero_ticket_assistenza_cliente(id_cliente):
    return len(TicketAssistenza.query.filter_by(id_cliente=id_cliente).all())


def get_ticket_assistenza_by_apicoltore(id_apicoltore):
    return TicketAssistenza.query.filter_by(id_apicoltore=id_apicoltore).all()


def get_ticket_assistenza_by_cliente(id_cliente):
    return TicketAssistenza.query.filter_by(id_cliente=id_cliente).all()


def get_ticket_by_id(id_ticket):
    return TicketAssistenza.query.filter_by(id=id_ticket).first()

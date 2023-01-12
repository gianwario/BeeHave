import datetime

from flask_login import current_user

from .. import db
from ..model.Apicoltore import Apicoltore
from ..model.TicketAssistenza import TicketAssistenza


def inserisci_area_assistenza(descrizione, assistenza):
    apicoltore = Apicoltore.query.filter_by(id=current_user.id).first()
    apicoltore.descrizione = descrizione
    apicoltore.assistenza = assistenza
    db.session.add(apicoltore)
    db.session.commit()


def get_assistenti():
    return Apicoltore.query.filter_by(assistenza=1).all()


# Controllo se l'apicoltore esiste ed è disponibile a fornire assistenza
def controlla_apicoltore(id_apicoltore):
    apicoltore = Apicoltore.query.filter_by(id=id_apicoltore).first()
    if apicoltore:
        return apicoltore.assistenza
    return False


def richiedi_assistenza(nome, descrizione, id_apicoltore):
    ticket = TicketAssistenza(id_cliente=current_user.id, id_apicoltore=id_apicoltore, nome=nome,
                              descrizione=descrizione, data_inizio=datetime.datetime.now(), stato='Creato')
    db.session.add(ticket)
    db.session.commit()

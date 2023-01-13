import datetime

from Website.flaskr import db
from Website.flaskr.model.Alveare import Alveare
from Website.flaskr.model.TicketAdozione import TicketAdozione


def inserisci_alveare(alveare):
    db.session.add(alveare)
    db.session.commit()


def get_alveare_by_id(alveare_id):
    return Alveare.query.filter_by(id=alveare_id).first()


def aggiorna_immagine_alveare(alveare_id, img):
    alveare = get_alveare_by_id(alveare_id)
    alveare.img_path = str(img)
    db.session.flush()
    db.session.commit()


def get_alveari():
    return Alveare.query.all()


def decrementa_percentuale(id_alveare, percentuale):
    alveare = Alveare.query.filter_by(id=id_alveare).first()
    alveare.percentuale_disponibile -= int(percentuale)
    db.session.flush()
    db.session.commit()


def affitto_alveare(ticket, percentuale):
    db.session.add(ticket)
    db.session.commit()
    decrementa_percentuale(ticket.id_alveare, percentuale)


def aggiorna_stato(alveare_id, covata_compatta, popolazione, polline, stato_cellette):
    alveare = get_alveare_by_id(alveare_id)
    alveare.covata_compatta = covata_compatta
    alveare.popolazione = popolazione
    alveare.polline = polline
    alveare.stato_cellette = stato_cellette
    db.session.flush()
    db.session.commit()
    # TODO eventualmente considerare di restituire la % allo scadere del tempo


def get_alveari_from_apicoltore(apicoltore_id):
    return Alveare.query.filter_by(id_apicoltore=apicoltore_id).all()


def get_ticket_adozione(cliente_id):
    return db.session.query(TicketAdozione, Alveare).filter_by(id_cliente=cliente_id).join(Alveare).all()


def get_ticket_from_alveare(id_alveare):
    return TicketAdozione.query.filter_by(id_alveare=id_alveare).all()


def controlla_scadenza_ticket(id_alveare):
    tickets = get_ticket_from_alveare(id_alveare)
    for ticket in tickets:
        if ticket.data_fine_adozione() > datetime.datetime.now():
            return False
    return True

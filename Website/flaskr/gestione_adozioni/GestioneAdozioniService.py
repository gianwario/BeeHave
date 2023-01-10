from sqlalchemy.orm import query

from Website.flaskr import db
from Website.flaskr.model.Alveare import Alveare
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.TicketAdozione import TicketAdozione


def inserisci_alveare(alveare):
    db.session.add(alveare)
    db.session.commit()


def get_alveareById(id):
    return Alveare.query.filter_by(id=id).first()


def update_imgAlveare(id, img):
    alveare = get_alveareById(id)
    alveare.img_path = str(img)
    db.session.flush()
    db.session.commit()


def get_AlveariDisponibili(apicoltore_id):
    lista = Alveare.query.filter_by(id_apicoltore=apicoltore_id).all()
    for alveare in lista:
        if alveare.percentuale_disponibile <= 0:
            lista.remove(alveare)
    return lista


def get_Alveari():
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
    # TODO eventualmente considerare di restituire la % allo scadere del tempo


def getAlveari_fromApicoltore(apicoltore_id):
    return Alveare.query.filter_by(id_apicoltore=apicoltore_id).all()


def getTicket_adozione(apicoltore_id):
    return db.session.query(TicketAdozione, Alveare).join(Alveare).filter_by(id_apicoltore=apicoltore_id).all()

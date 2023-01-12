from Website.flaskr import db
from Website.flaskr.model.Alveare import Alveare
from Website.flaskr.model.TicketAdozione import TicketAdozione


def inserisci_alveare(alveare):
    db.session.add(alveare)
    db.session.commit()


def get_alveare_by_id(alveare_id):
    return Alveare.query.filter_by(id=alveare_id).first()


def update_img_alveare(alveare_id, img):
    alveare = get_alveare_by_id(alveare_id)
    alveare.img_path = str(img)
    db.session.flush()
    db.session.commit()


def get_alveari_disponibili(apicoltore_id):
    lista = Alveare.query.filter_by(id_apicoltore=apicoltore_id).all()
    for alveare in lista:
        if alveare.percentuale_disponibile <= 0:
            lista.remove(alveare)
    return lista


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
    # TODO eventualmente considerare di restituire la % allo scadere del tempo


def get_alveari_from_apicoltore(apicoltore_id):
    return Alveare.query.filter_by(id_apicoltore=apicoltore_id).all()


def get_ticket_adozione(apicoltore_id):
    return db.session.query(TicketAdozione, Alveare).join(Alveare).filter_by(id_apicoltore=apicoltore_id).all()

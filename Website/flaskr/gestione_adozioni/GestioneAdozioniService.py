from Website.flaskr import db
from Website.flaskr.model.Alveare import Alveare


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

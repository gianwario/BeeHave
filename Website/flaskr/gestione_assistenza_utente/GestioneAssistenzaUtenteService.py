from flask_login import current_user

from .. import db
from ..model.Apicoltore import Apicoltore


def inserisci_area_assistenza(descrizione, assistenza):
    apicoltore = Apicoltore.query.filter_by(id=current_user.id).first()
    apicoltore.descrizione = descrizione
    apicoltore.assistenza = assistenza
    db.session.add(apicoltore)
    db.session.commit()

from flask_login import current_user

from .. import db
from ..model.Apicoltore import Apicoltore


def crea_area_assistenza(descrizione):
    apicoltore = Apicoltore.query.filterById(id=current_user.id).first()
    apicoltore.descrizione = descrizione
    apicoltore.assistenza = True
    db.session.add(apicoltore)
    db.session.commit()

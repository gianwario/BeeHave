from Website.flaskr import db
from Website.flaskr.model.Alveare import Alveare


def inserisci_alveare(nome, produzione, numero_api, tipo_miele, percentuale_disponibile,
                          covata_compatta, prezzo, tipo_fiore, popolazione, polline, stato_cellette, apicoltore):
    alveare = Alveare(nome=nome, produzione= produzione, numero_api= numero_api, tipo_miele=tipo_miele,percentuale_disponibile= percentuale_disponibile,
                      covata_compatta=covata_compatta, prezzo = prezzo, tipo_fiore= tipo_fiore,popolazione= popolazione, polline=polline,
                      stato_cellette=stato_cellette,id_apicoltore= apicoltore)
    db.session.add(alveare)
    db.session.commit()

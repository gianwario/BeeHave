from Website.flaskr import db
from Website.flaskr.model.Prodotto import Prodotto


def inserisci_prodotto(nome, descrizione, localita, peso, tipologia, prezzo, quantita, apicoltore):
    prodotto = Prodotto(nome=nome, descrizione=descrizione,
                        localita=localita, peso=peso, tipologia=tipologia, prezzo=prezzo, quantita=quantita, apicoltore=apicoltore)
    db.session.add(prodotto)
    db.session.commit()
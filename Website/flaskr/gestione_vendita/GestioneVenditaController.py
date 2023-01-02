from flask import Blueprint, request, session
from flask_login import current_user, login_required

from Website.flaskr.Routes import catalogo_apicoltore
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto

gv = Blueprint('gv', __name__)


@gv.route('/inserimento_prodotto', methods=['GET', 'POST'])
@login_required
def inserimento_prodotto():
    if request.method == 'POST' and session['isApicoltore']:
        nome = request.form.get('nome')
        descrizione = request.form.get('descrizione')
        localita = request.form.get('localita')
        peso = request.form.get('peso')
        tipologia = request.form.get('tipologia')
        prezzo = request.form.get('prezzo')
        quantita = request.form.get('quantita')
        apicoltore = current_user.id

        inserisci_prodotto(nome, descrizione,localita,peso, tipologia,prezzo, quantita, apicoltore)

    return catalogo_apicoltore()

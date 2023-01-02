from flask import Blueprint, request, session, render_template
from flask_login import current_user, login_required

from Website.flaskr.Routes import catalogo_apicoltore
from Website.flaskr.gestione_utente.GestioneUtenteService import getApicoltoreById
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, getProdottoById

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

@gv.route('/visualizza_prod/<int:prodotto_id>', methods=['POST', 'GET'])
def info_articolo(prodotto_id):
    prod = getProdottoById(prodotto_id)
    #apicoltore = getApicoltoreById(prod.id_apicoltore)
    return render_template('informazioni_prodotto.html', prodotto=prod)
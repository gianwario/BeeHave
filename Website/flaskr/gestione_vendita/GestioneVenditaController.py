from flask import Blueprint, request, session
from flask_login import current_user, login_required

from Website.flaskr.Routes import mostra_prodotti, mostra_articoli_in_vendita, info_articolo, inserimento_prodotto_page
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, cancella_prodotto, \
    acquisto_prodotto

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
        if not inserisci_prodotto(nome, descrizione, localita, peso, tipologia, prezzo, quantita):
            return inserimento_prodotto_page()
    return mostra_articoli_in_vendita(current_user.id)


@gv.route('/elimina_prodotto/<int:id_prodotto>/<int:id_apicoltore>', methods=['POST', 'GET'])
@login_required
def elimina_prodotto(id_prodotto, id_apicoltore):
    if session['isApicoltore'] and id_apicoltore == current_user.id:
        cancella_prodotto(id_prodotto)
        return mostra_articoli_in_vendita(current_user.id)


@gv.route('/acquista_prodotto', methods=['POST', 'GET'])
@login_required
def acquista_prodotto():
    if request.method == 'POST' and not session['isApicoltore']:
        quantita = request.form.get('quantita_prod')
        id_prodotto = request.form.get('id_prd')

        if acquisto_prodotto(id_prodotto=id_prodotto, quantita=quantita):
            return info_articolo(id_prodotto)
    return mostra_prodotti()

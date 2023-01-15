from flask import Blueprint, request, session, flash
from flask_login import current_user, login_required

from Website.flaskr.Routes import mostra_prodotti, mostra_articoli_in_vendita, info_articolo
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, cancella_prodotto, \
    acquisto_prodotto, get_prodotto_by_id
from Website.flaskr.model.Acquisto import Acquisto
from Website.flaskr.model.Prodotto import Prodotto

gv = Blueprint('gv', __name__)


@gv.route('/inserimento_prodotto', methods=['GET', 'POST'])
@login_required
def inserimento_prodotto():
    if request.method == 'POST' and session['isApicoltore']:
        nome = request.form.get('nome')
        descrizione = request.form.get('descrizione')
        localita = request.form.get('localita')
        peso = int(request.form.get('peso'))
        tipologia = request.form.get('tipologia')
        prezzo = float(request.form.get('prezzo'))
        quantita = int(request.form.get('quantita'))
        apicoltore = current_user.id

        if not 0 < len(nome) <= 30:
            flash('Lunghezza nome non valida!', category='error')
        elif not 0 < len(descrizione) <= 200:
            flash('Lunghezza descrizione non valida!', category='error')
        elif not 0 < len(localita) <= 40:
            flash('Lunghezza località non valida!', category='error')
        elif not 0 < peso <= 1000:
            flash('Peso non è nel range corretto', category='error')
        elif not 0 < len(tipologia) <= 30:
            flash('Lunghezza tipologia non valida!', category='error')
        elif not 0 < prezzo <= 1000:
            flash('Prezzo non è nel range corretto!', category='error')
        elif not 0 < quantita <= 1000000:
            flash('Quantità non è nel range corretto!', category='error')
        else:
            flash('Inserimento avvenuto con successo!', category='success')

            prod = Prodotto(nome=nome, descrizione=descrizione, localita=localita, peso=peso, prezzo=prezzo,
                            quantita=quantita, id_apicoltore=apicoltore, tipologia=tipologia)

            inserisci_prodotto(prod)
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
        quantita = int(request.form.get('quantita_prod'))
        id_cliente = int(request.form.get('id_client'))
        id_prodotto = int(request.form.get('id_prd'))
        quantita_articolo = get_prodotto_by_id(id_prodotto).quantita
        if quantita > quantita_articolo:
            flash('Quantitá non disponibile!', category='error')
        else:
            acquisto = Acquisto(id_cliente=id_cliente, id_prodotto=id_prodotto, quantita=quantita)
            acquisto_prodotto(acquisto, quantita)
            flash('Acquisto andato a buon fine!',category='success')
            return info_articolo(id_prodotto)
    return mostra_prodotti()

from datetime import datetime

from flask import Blueprint, request, session, flash
from flask_login import login_required, current_user

from Website.flaskr.Routes import mostra_alveari
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, affitto_alveare, aggiorna_stato
from Website.flaskr.model.Alveare import Alveare
from Website.flaskr.model.TicketAdozione import TicketAdozione

ga = Blueprint('ga', __name__)


@ga.route('/inserimento_alveare', methods=['GET', 'POST'])
@login_required
def inserimento_alveare():
    if request.method == 'POST' and session['isApicoltore']:
        nome = request.form.get('nome')
        produzione = int(request.form.get('produzione'))
        numero_api = int(request.form.get('numero_api'))
        tipo_miele = request.form.get('tipo_miele')
        tipo_fiore = request.form.get('tipo_fiore')
        prezzo = float(request.form.get('prezzo'))
        apicoltore = current_user.id

        if not 0 < len(nome) <= 30:
            flash('Lunghezza Nome non valida!', category='error')
        elif not 0 < len(tipo_fiore) <= 30:
            flash('Lunghezza di TipoFiore non valida!', category='error')
        elif not 0 < produzione <= 2000:
            flash('Quantità produzione non è nel range corretto!', category='error')
        elif not 0 < len(tipo_miele) <= 30:
            flash('Lunghezza di TipoMiele non valida!', category='error')
        elif not 0 < numero_api <= 40000:
            flash('NumeroApi non è nel range corretto!', category='error')
        elif not 0 < prezzo <= 1000:
            flash('Prezzo non è nel range corretto!', category='error')
        else:
            flash('Inserimento avvenuto con successo!', category='success')

            alveare = Alveare(nome=nome, produzione=produzione, numero_api=numero_api, tipo_miele=tipo_miele,
                              percentuale_disponibile=100,
                              prezzo=prezzo, tipo_fiore=tipo_fiore, id_apicoltore=apicoltore)

            inserisci_alveare(alveare)

    return mostra_alveari()


@ga.route('/modifica_stato_alveare', methods=['GET', 'POST'])
@login_required
def modifica_stato_alveare():
    if request.method == 'POST' and session['isApicoltore']:
        covata_compatta = request.form.get('covata_compatta')
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        stato_larve = request.form.get('stato_larve')
        alveare_id = request.form.get('alveare_id')

        if covata_compatta == '':
            flash('CovataCompatta non è stata inserita!', category='error')
        elif not 0 < len(popolazione) <= 30:
            flash('Lunghezza di Popolazione non valida!', category='error')
        elif not 0 < len(polline) <= 2000:
            flash('Lunghezza di Polline non valida!', category='error')
        elif not 0 < len(stato_cellette) <= 30:
            flash('Lunghezza di Stato Cellette non valida!', category='error')
        elif not 0 < len(stato_larve) <= 30:
            flash('Lunghezza di Stato Larve non valida!', category='error')
        else:
            aggiorna_stato(alveare_id, int(covata_compatta), popolazione, polline, stato_cellette, stato_larve)
            flash('Stato alveare aggiornato correttamente', category='success')
    return mostra_alveari()


@ga.route('/adotta_alveare', methods=['POST', 'GET'])
@login_required
def adotta_alveare():
    if request.method == 'POST' and not session['isApicoltore']:
        percentuale = int(request.form.get('disp'))
        id_alveare = int(request.form.get('id_alv'))
        percentuale_residua = int(request.form.get('percentuale_residua'))
        id_cliente = int(request.form.get('id_client'))
        tempo_adozione = int(request.form.get('tempo_adozione'))
        if percentuale > percentuale_residua:
            flash('Quantitá non disponibile!', category='error')
        else:
            ticket = TicketAdozione(id_cliente=id_cliente, id_alveare=id_alveare, percentuale_adozione=percentuale,
                                    data_inizio_adozione=datetime.now(), tempo_adozione=tempo_adozione)
            affitto_alveare(ticket, percentuale)
    return mostra_alveari()

from flask import Blueprint, request, session
from flask_login import login_required

from Website.flaskr.Routes import mostra_alveari, modifica_stato, home, informazioni_alveare, inserimento_alveare_page
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, adozione_alveare, \
    aggiorna_stato, get_alveare_by_id

ga = Blueprint('ga', __name__)


@ga.route('/inserimento_alveare', methods=['GET', 'POST'])
@login_required
def inserimento_alveare():
    if request.method == 'POST' and session['isApicoltore']:
        nome = request.form.get('nome')
        produzione = request.form.get('produzione')
        numero_api = request.form.get('numero_api')
        tipo_miele = request.form.get('tipo_miele')
        tipo_fiore = request.form.get('tipo_fiore')
        prezzo = request.form.get('prezzo')

        if not inserisci_alveare(nome=nome, produzione=produzione, numero_api=numero_api, tipo_miele=tipo_miele,
                                 prezzo=prezzo, tipo_fiore=tipo_fiore):
            return inserimento_alveare_page()

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
        alveare = get_alveare_by_id(alveare_id)
        if alveare is not None:
            if aggiorna_stato(alveare, covata_compatta, popolazione, polline, stato_cellette, stato_larve):
                return informazioni_alveare(alveare_id)
        return modifica_stato(alveare_id)
    return home()


@ga.route('/adotta_alveare', methods=['POST', 'GET'])
@login_required
def adotta_alveare():
    if request.method == 'POST' and not session['isApicoltore']:
        tempo_adozione = request.form.get('tempo_adozione')
        percentuale = request.form.get('disp')
        id_alveare = request.form.get('id_alv')

        adozione_alveare(percentuale=percentuale, tempo_adozione=tempo_adozione, id_alveare=id_alveare)

        return informazioni_alveare(id_alveare)
    return mostra_alveari()

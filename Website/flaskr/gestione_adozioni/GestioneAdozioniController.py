from flask import Blueprint, request, session
from flask_login import login_required, current_user

from Website.flaskr.Routes import inserimento_alveare_page
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare
from Website.flaskr.model.Alveare import Alveare

ga = Blueprint('ga', __name__)


@ga.route('/inserimento_alveare', methods=['GET', 'POST'])
@login_required
def inserimento_alveare():
    if request.method == 'POST':
        nome = request.form.get('nome')
        produzione = int(request.form.get('produzione'))
        numero_api = int(request.form.get('numero_api'))
        tipo_miele = request.form.get('tipo_miele')
        percentuale_disponibile = "100%"
        covata_compatta = int(request.form.get('covata_compatta'))
        tipo_fiore = request.form.get('tipo_fiore')
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        apicoltore = current_user.id

        inserisci_alveare(nome, produzione, numero_api, tipo_miele, percentuale_disponibile,
                          covata_compatta, tipo_fiore, popolazione, polline, stato_cellette, apicoltore)


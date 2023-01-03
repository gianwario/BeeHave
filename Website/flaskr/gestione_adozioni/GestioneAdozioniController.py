from flask import Blueprint, request, session, flash
from flask_login import login_required, current_user

from Website.flaskr.Routes import inserimento_alveare_page
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare
from Website.flaskr.model.Alveare import Alveare

ga = Blueprint('ga', __name__)


@ga.route('/inserimento_alveare', methods=['GET', 'POST'])
def inserimento_alveare():
    if request.method == 'POST':
        nome = request.form.get('nome')
        produzione = int(request.form.get('produzione'))
        numero_api = int(request.form.get('numero_api'))
        tipo_miele = request.form.get('tipo_miele')
        percentuale_disponibile = "100%"
        covata_compatta = int(request.form.get('covata_compatta'))
        tipo_fiore = request.form.get('tipo_fiore')
        prezzo: int = int(request.form.get('prezzo'))
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        apicoltore = current_user.id

        if (len(nome) > 30):
            flash('Nome troppo lungo!', category='error')
        elif (len(tipo_fiore) > 30):
            flash('Fiore invalido!', category='error')
        elif (len(tipo_miele) > 30):
            flash('Miele invalido!', category='error')
        elif (prezzo > 1000):
            flash('Prezzo troppo alto!', category='error')
        else:
            inserisci_alveare(nome, produzione, numero_api, tipo_miele, percentuale_disponibile,
                              covata_compatta, prezzo, tipo_fiore, popolazione, polline, stato_cellette, apicoltore)
            flash('Inserimento alveare avvenuto con successo!', category='success')

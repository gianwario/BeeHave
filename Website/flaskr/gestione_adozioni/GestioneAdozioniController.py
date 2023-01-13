import os
from datetime import datetime

from flask import Blueprint, request, session, flash, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import mostra_alveari
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, aggiorna_immagine_alveare, \
    affitto_alveare, aggiorna_stato
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
        percentuale_disponibile = 100
        covata_compatta = int(request.form.get('covata_compatta'))
        tipo_fiore = request.form.get('tipo_fiore')
        prezzo: int = int(request.form.get('prezzo'))
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        apicoltore = current_user.id

        if len(nome) > 30:
            flash('Nome troppo lungo!', category='error')
        elif len(tipo_fiore) > 30:
            flash('Fiore invalido!', category='error')
        elif len(tipo_miele) > 30:
            flash('Miele invalido!', category='error')
        elif prezzo > 1000:
            flash('Prezzo troppo alto!', category='error')
        else:
            flash('Inserimento avvenuto con successo!', category='success')

            alveare = Alveare(nome=nome, produzione=produzione, numero_api=numero_api, tipo_miele=tipo_miele,
                              percentuale_disponibile=percentuale_disponibile,
                              covata_compatta=covata_compatta, prezzo=prezzo, tipo_fiore=tipo_fiore,
                              popolazione=popolazione, polline=polline,
                              stato_cellette=stato_cellette, id_apicoltore=apicoltore, img_path='value')

            inserisci_alveare(alveare)

            image = request.files['imagepath']
            if image == '':
                nome_alv = 'alveare' + str(alveare.id) + ".jpg"
                path_image = os.path.join(image_folder_absolute, secure_filename(image.filename))
                image.save(path_image)
                os.rename(path_image, os.path.join(image_folder_absolute, nome_alv))
                aggiorna_immagine_alveare(alveare.id, nome_alv)

    return mostra_alveari()


@ga.route('/modifica_stato_alveare', methods=['GET', 'POST'])
@login_required
def modifica_stato_alveare():
    if request.method == 'POST' and session['isApicoltore']:
        covata_compatta = int(request.form.get('covata_compatta'))
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        alveare_id = request.form.get('alveare_id')
        aggiorna_stato(alveare_id, covata_compatta, popolazione, polline, stato_cellette)
        flash('Stato alveare aggiornato correttamente', category='success')
        return render_template('/catalogo_alveari_apicoltore.html')
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

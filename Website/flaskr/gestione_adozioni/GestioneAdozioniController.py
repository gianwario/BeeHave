import os
from datetime import datetime

from flask import Blueprint, request, session, flash, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import mostra_alveari, home
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, update_img_alveare, \
    get_alveari_disponibili, get_alveare_by_id, affitto_alveare, get_ticket_adozione, aggiorna_stato
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_id, get_cliente_by_id
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
            nome_alv = 'alveare' + str(alveare.id) + ".jpg"
            path_image = os.path.join(image_folder_absolute, secure_filename(image.filename))
            image.save(path_image)
            os.rename(path_image, os.path.join(image_folder_absolute, nome_alv))
            update_img_alveare(alveare.id, nome_alv)
            # TODO fixare formati immagini, non basta solo jpg
    return mostra_alveari_disponibili()


@ga.route('/visualizza_alveari_disponibili', methods=['GET', 'POST'])
@login_required
def mostra_alveari_disponibili():
    if session['isApicoltore']:
        alveari_disponibili = get_alveari_disponibili(current_user.id)
        return render_template('/catalogo_alveari_disponibili.html', alveari_disponibili=alveari_disponibili)


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
        return render_template('/catalogo_alveari_disponibili.html')
    return mostra_alveari()


@ga.route('/informazioni_alveare/<int:alveare_id>', methods=['POST', 'GET'])
def informazioni_alveare(alveare_id):
    alveare = get_alveare_by_id(alveare_id)
    apicoltore = get_apicoltore_by_id(alveare.id_apicoltore)
    return render_template('informazioni_alveare.html', alveare=alveare, apicoltore=apicoltore)


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

        ticket = TicketAdozione(id_cliente=id_cliente, id_alveare=id_alveare, percentuale_adozione=percentuale,
                                data_inizio_adozione=datetime.date.today(), tempo_adozione=tempo_adozione)
        affitto_alveare(ticket, percentuale)
        return mostra_alveari()


@ga.route('/alveari_adottati/<int:apicoltore_id>', methods=['GET'])
@login_required
def mostra_alveari_adottati(apicoltore_id):
    if not session['isApicoltore']:
        lista_clienti = []
        alveari_adottati = get_ticket_adozione(apicoltore_id)
        for x in alveari_adottati:
            lista_clienti.append(get_cliente_by_id(x.TicketAdozione.id_cliente))

        return render_template('alveari_adottati.html', alveari_adottati=alveari_adottati, lista_clienti=lista_clienti)
    return home()

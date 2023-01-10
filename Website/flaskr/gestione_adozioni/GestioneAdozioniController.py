import datetime
import os

from flask import Blueprint, request, session, flash, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import date
from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import inserimento_alveare_page, mostra_alveari
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, update_imgAlveare, \
    get_AlveariDisponibili, get_alveareById, affitto_alveare, get_Alveari, getTicket_adozione
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_id, get_cliente_by_id
from Website.flaskr.model.TicketAdozione import TicketAdozione
from Website.flaskr.model.Alveare import Alveare

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

        if (len(nome) > 30):
            flash('Nome troppo lungo!', category='error')
        elif (len(tipo_fiore) > 30):
            flash('Fiore invalido!', category='error')
        elif (len(tipo_miele) > 30):
            flash('Miele invalido!', category='error')
        elif (prezzo > 1000):
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
        update_imgAlveare(alveare.id, nome_alv)
        # TODO fixare formati immagini, non basta solo jpg
    return mostra_alveari_disponibili(current_user.id)


@ga.route('/visualizza_alveari_disponibili/<int:apicoltore_id>', methods=['POST', 'GET'])
@login_required
def mostra_alveari_disponibili(apicoltore_id):
    if session['isApicoltore']:
        alveari_disponibili = get_AlveariDisponibili(apicoltore_id)
        return render_template('/catalogo_alveari_disponibili.html', alveari_disponibili=alveari_disponibili)


@ga.route('/informazioni_alveare/<int:alveare_id>', methods=['POST', 'GET'])
def informazioni_alveare(alveare_id):
    alveare = get_alveareById(alveare_id)
    apicoltore = get_apicoltore_by_id(alveare.id_apicoltore)
    return render_template('informazioni_alveare.html', alveare=alveare, apicoltore=apicoltore)


@ga.route('/affitta_alveare', methods=['POST', 'GET'])
@login_required
def affitta_alveare():
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

@ga.route('/alveari_affittati/<int:apicoltore_id>', methods=['GET'])
def mostra_alveari_affittati(apicoltore_id):
    lista_clienti = []
    #if not current_user.is_authenticated or not session['isApicoltore']:
    alveari_affittati = getTicket_adozione(apicoltore_id)
    for x in alveari_affittati:
        lista_clienti.append(get_cliente_by_id(x.TicketAdozione.id_cliente))

    return render_template('alveari_affittati.html', alveari_affittati=alveari_affittati, lista_clienti=lista_clienti)
    #return home()
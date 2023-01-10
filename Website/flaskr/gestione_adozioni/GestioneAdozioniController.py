import os

from flask import Blueprint, request, session, flash, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import inserimento_alveare_page, mostra_alveari
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, update_imgAlveare, \
    get_AlveariDisponibili, update_Stato
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
    return mostra_alveari_disponibili()


@ga.route('/visualizza_alveari_disponibili', methods=['GET', 'POST'])
@login_required
def mostra_alveari_disponibili():
    if session['isApicoltore']:
        alveari_disponibili = get_AlveariDisponibili(current_user.id)
        return render_template('/catalogo_alveari_disponibili.html', alveari_disponibili=alveari_disponibili)


@ga.route('/modifica_stato_alveare', methods=['GET', 'POST'])
@login_required
def modifica_stato_alveare():
    if request.method=='POST' and session['isApicoltore']:
        covata_compatta = int(request.form.get('covata_compatta'))
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        alveare_id = request.form.get('alveare_id')
        update_Stato(alveare_id, covata_compatta, popolazione, polline, stato_cellette)
        flash('Stato alveare aggiornato correttamente', category='success')
        return render_template('/catalogo_alveari_disponibili.html')
    return mostra_alveari()

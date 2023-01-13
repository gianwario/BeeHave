import os

from flask import Blueprint, request, session, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import mostra_prodotti, mostra_articoli_in_vendita
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, aggiorna_immagine, \
    cancella_prodotto, acquisto_prodotto
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

        if len(nome) > 30:
            flash('Nome troppo lungo!', category='error')
        elif len(descrizione) > 200:
            flash('Descrizione troppo lunga!', category='error')
        elif len(localita) > 40:
            flash('Località invalida!', category='error')
        elif prezzo > 1000:
            flash('Prezzo invalido!', category='error')
        elif len(tipologia) > 30:
            flash('Nome tipologia lungo!', category='error')
        elif quantita > 1000000:
            flash('Quantità invalida!', category='error')
        else:
            flash('Inserimento avvenuto con successo!', category='success')

        prod = Prodotto(nome=nome, descrizione=descrizione, localita=localita, peso=peso, img_path='ssd', prezzo=prezzo,
                        quantita=quantita, id_apicoltore=apicoltore, tipologia=tipologia)

        inserisci_prodotto(prod)

        image = request.files['imagepath']
        if image == '':
            nome_vasetto = 'honey_pot' + str(prod.id) + ".jpg"
            path_image = os.path.join(image_folder_absolute, secure_filename(image.filename))
            image.save(path_image)
            os.rename(path_image, os.path.join(image_folder_absolute, nome_vasetto))
            aggiorna_immagine(prod.id, nome_vasetto)
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
        qnt_articolo = int(request.form.get('qnt_articolo'))
        id_cliente = int(request.form.get('id_client'))
        id_prodotto = int(request.form.get('id_prd'))
        if quantita > qnt_articolo:
            flash('Quantitá non disponibile!', category='error')

        acquisto = Acquisto(id_cliente=id_cliente, id_prodotto=id_prodotto, quantita=quantita)
        acquisto_prodotto(acquisto, quantita)
    return mostra_prodotti()

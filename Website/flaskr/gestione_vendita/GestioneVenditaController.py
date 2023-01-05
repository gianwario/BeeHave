from flask import Blueprint, request, session, render_template, flash
from flask_login import current_user, login_required
import os

from werkzeug.utils import secure_filename
from Website.flaskr import image_folder_absolute
from Website.flaskr.Routes import area_personale, home, mostra_prodotti
from Website.flaskr.gestione_utente.GestioneUtenteService import getApicoltoreById
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, getProdottoById, updateImage, \
    get_ProdottiByApicoltore, deleteProdotto, acquisto_prodotto
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

        if (len(nome) > 30):
            flash('Nome troppo lungo!', category='error')
        elif (len(descrizione) > 200):
            flash('Descrizione troppo lunga!', category='error')
        elif (len(localita) > 40):
            flash('Località invalida!', category='error')
        elif (prezzo > 1000):
            flash('Prezzo invalido!', category='error')
        elif (len(tipologia) > 30):
            flash('Nome tipologia lungo!', category='error')
        elif (quantita > 1000000):
            flash('Quantità invalida!', category='error')
        else:
            flash('Inserimento avvenuto con successo!', category='success')

        prod = Prodotto(nome=nome, descrizione=descrizione, localita=localita, peso=peso, img_path='ssd', prezzo=prezzo,
                        quantita=quantita, id_apicoltore=apicoltore, tipologia=tipologia)

        inserisci_prodotto(prod)

        image = request.files['imagepath']
        nome_vasetto = 'honey_pot' + str(prod.id) + ".jpg"
        path_image = os.path.join(image_folder_absolute, secure_filename(image.filename))
        image.save(path_image)
        os.rename(path_image, os.path.join(image_folder_absolute, nome_vasetto))
        updateImage(prod.id, nome_vasetto)
        # TODO fixare formati immagini, non basta solo jpg
    return mostra_articoli_inVendita(current_user.id)


@gv.route('/visualizza_prod/<int:prodotto_id>', methods=['POST', 'GET'])
def info_articolo(prodotto_id):
    prod = getProdottoById(prodotto_id)
    apicoltore = getApicoltoreById(prod.id_apicoltore)
    return render_template('informazioni_prodotto.html', prodotto=prod, apicoltore=apicoltore)


@gv.route('/visualizza_prodotti_vendita/<int:apicoltore_id>', methods=['POST', 'GET'])
@login_required
def mostra_articoli_inVendita(apicoltore_id):
    if session['isApicoltore']:
        prodotti_in_vendita = get_ProdottiByApicoltore(apicoltore_id)
        return render_template('/catalogo_apicoltore.html', prodotti_in_vendita=prodotti_in_vendita)


@gv.route('/elimina_prodotto/<int:id_prodotto>/<int:id_api>', methods=['POST', 'GET'])
@login_required
def elimina_prodotto(id_prodotto, id_api):
    if session['isApicoltore']:
        prod = getProdottoById(id_prodotto)
        path = os.path.join(image_folder_absolute, prod.img_path)
        os.remove(path)
        deleteProdotto(id_prodotto)
        # prodotti_in_vendita = get_ProdottiByApicoltore(id_api)
        # return render_template('/catalogo_apicoltore.html', prodotti_in_vendita=prodotti_in_vendita)
        return area_personale()
        # TODO fix refresh page


@gv.route('/acquista_prodotto', methods=['POST', 'GET'])
@login_required
def acquista_prodotto():
    if request.method == 'POST':  # TODO Add session isCliente
        quantita = int(request.form.get('quantita_prod'))
        print(quantita)
        qnt_articolo = int(request.form.get('qnt_articolo'))
        print(qnt_articolo)
        id_cliente = int(request.form.get('id_client'))
        print(id_cliente)

        id_prodotto = int(request.form.get('id_prd'))
        print(id_prodotto)
        if quantita <= qnt_articolo:
            flash('Quantitá non disponibile!', category='error')

        acquisto = Acquisto(id_cliente=id_cliente, id_prodotto=id_prodotto)
        acquisto_prodotto(acquisto, quantita)
    return mostra_prodotti()

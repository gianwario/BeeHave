from flask import Blueprint, request, session, render_template, flash
from flask_login import current_user, login_required
import os
from pathlib import Path
from werkzeug.utils import secure_filename

from Website.flaskr.Routes import catalogo_apicoltore
from Website.flaskr.gestione_utente.GestioneUtenteService import getApicoltoreById
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, getProdottoById
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
        destination = r"C:\Users\Cosmo\OneDrive\Documents\GitHub\BeeHave\Website\flaskr\static\images"
        nome_vasetto = 'honey_pot' + str(prod.id)
        os.rename(destination + str(image.filename), destination + nome_vasetto)
        image.save(os.path.join(destination, secure_filename(image.filename)))

    return catalogo_apicoltore()


@gv.route('/visualizza_prod/<int:prodotto_id>', methods=['POST', 'GET'])
def info_articolo(prodotto_id):
    prod = getProdottoById(prodotto_id)
    apicoltore = getApicoltoreById(prod.id_apicoltore)
    return render_template('informazioni_prodotto.html', prodotto=prod, apicoltore=apicoltore)

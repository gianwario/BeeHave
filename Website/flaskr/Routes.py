from flask import render_template, Blueprint
from flask_login import login_required
from flask_login import current_user

from Website.flaskr.gestione_adozioni.GestioneAdozioniService import get_Alveari
from Website.flaskr.gestione_vendita.GestioneVenditaService import getTuttiProdotti, getProdottoById
from Website.flaskr.model.Prodotto import Prodotto

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/login_page')
def login_page():
    if current_user.is_authenticated:
        return home()
    return render_template('login_page.html')

@views.route('/inserimento_prodotto_page')
def inserimento_prodotto_page():
    return render_template('inserimento_prodotto.html')


@views.route('/inserimento_alveare_page')
def inserimento_alveare_page():
    return render_template('inserimento_alveare.html')


@views.route('/registrazione_cl')
def sigup_cl(): #typo, da cambiare
    return render_template('registrazione_cliente.html')
    
@views.route('/registrazione_apicoltore')
def sigup_ap():
    return render_template('registrazione_apicoltore.html')
@views.route('/areapersonale')
@login_required
def area_personale():
    return render_template('areapersonale.html')


@views.route('/catalogo_prod', methods=['GET'])
def mostra_prodotti():
    prods = getTuttiProdotti()
    return render_template('catalogo_prodotti.html', prods=prods)


@views.route('/catalogo_alveari', methods=['GET'])
def mostra_alveari():
    alveari_disponibili = get_Alveari()
    return render_template('catalogo_alveari.html', alveari_disponibili=alveari_disponibili)

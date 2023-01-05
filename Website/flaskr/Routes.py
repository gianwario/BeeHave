from flask import render_template, Blueprint, session
from flask_login import login_required,current_user

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
@login_required
def inserimento_prodotto_page():
    if session['isApicoltore']:
        return render_template('inserimento_prodotto.html')
    return home()

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
    if session['isApicoltore']:
        return render_template('areapersonale.html')
    return render_template('area_personale_cliente.html')

@views.route('/tester')
def test_template():
    alveari_disponibili = get_Alveari()
    return render_template('test.html', alveari_disponibili=alveari_disponibili)


@views.route('/catalogo_prod')
def mostra_prodotti():
    prods = getTuttiProdotti()
    return render_template('catalogo_prodotti.html', prods=prods)


@views.route('/crea_area_assistenza_page')
@login_required
def crea_area_assistenza_page():
    if session['isApicoltore'] and not current_user.assistenza:
        return render_template('creazione_area_assistenza.html')
    return home()
    
@views.route('/catalogo_alveari', methods=['GET'])
def mostra_alveari():
    alveari_disponibili = get_Alveari()
    return render_template('catalogo_alveari.html', alveari_disponibili=alveari_disponibili)

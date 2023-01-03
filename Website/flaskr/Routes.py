from flask import render_template, Blueprint

from Website.flaskr.gestione_vendita.GestioneVenditaService import getTuttiProdotti, getProdottoById
from Website.flaskr.model.Prodotto import Prodotto

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')


@views.route('/catalogo_apicoltore')
def catalogo_apicoltore():
    return render_template('/catalogo_apicoltore.html')


@views.route('/inserimento_prodotto_page')
def inserimento_prodotto_page():
    return render_template('inserimento_prodotto.html')


@views.route('/inserimento_alveare_page')
def inserimento_alveare_page():
    return render_template('inserimento_alveare.html')


@views.route('/registrazione_apicoltore')
def sigup_ap():
    return render_template('registrazione_apicoltore.html')


@views.route('/catalogo_prod', methods=['GET'])
def mostra_prodotti():
    prods = getTuttiProdotti()
    return render_template('catalogo_prodotti.html', prods=prods)




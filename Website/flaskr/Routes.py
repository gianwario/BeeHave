from flask import render_template, Blueprint, session
from flask_login import login_required, current_user

from Website.flaskr.gestione_adozioni.GestioneAdozioniService import get_alveari
from Website.flaskr.gestione_assistenza_utente.GestioneAssistenzaUtenteService import get_assistenti
from Website.flaskr.gestione_vendita.GestioneVenditaService import get_tutti_prodotti, get_prodotti_by_apicoltore

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/login_page')
def login_page():
    if not current_user.is_authenticated:
        return render_template('login_page.html')
    return home()


@views.route('/inserimento_prodotto_page')
@login_required
def inserimento_prodotto_page():
    if session['isApicoltore']:
        return render_template('inserimento_prodotto.html')
    return home()


@views.route('/inserimento_alveare_page')
@login_required
def inserimento_alveare_page():
    if session['isApicoltore']:
        return render_template('inserimento_alveare.html')
    return home()


@views.route('/registrazione_cliente')
def registrazione_cliente_page():
    if not current_user.is_authenticated:
        return render_template('registrazione_cliente.html')
    return home()


@views.route('/registrazione_apicoltore')
def registrazione_apicoltore_page():
    if not current_user.is_authenticated:
        return render_template('registrazione_apicoltore.html')
    return home()


@views.route('/areapersonale')
@login_required
def area_personale():
    if session['isApicoltore']:
        return render_template('areapersonale.html')
    return render_template('area_personale_cliente.html')


@views.route('/catalogo_prodotti')
def mostra_prodotti():
    if not current_user.is_authenticated or not session['isApicoltore']:
        prodotti = get_tutti_prodotti()
        return render_template('catalogo_prodotti.html', prodotti=prodotti)
    prodotti = get_prodotti_by_apicoltore()
    return render_template('catalogo_prodotti_apicoltore.html', prodotti_in_vendita=prodotti)


@views.route('/modifica_dati_utente_page')
@login_required
def modifica_dati_utente_page():
    return render_template("modifica_dati_utente.html")


@views.route('/crea_area_assistenza_page')
@login_required
def crea_area_assistenza_page():
    if session['isApicoltore'] and not current_user.assistenza:
        return render_template('creazione_area_assistenza.html')
    return home()


@views.route('/catalogo_alveari')
def mostra_alveari():
    if not current_user.is_authenticated or not session['isApicoltore']:
        alveari_disponibili = get_alveari()
        return render_template('catalogo_alveari.html', alveari_disponibili=alveari_disponibili)
    return render_template('alveari_adottati.html')


@views.route('/richiesta_assistenza_page/<int:id_apicoltore>')
@login_required
def richiesta_assistenza_page(id_apicoltore):
    if not session['isApicoltore']:
        return render_template('richiedi_assistenza.html', id_apicoltore=id_apicoltore)
    return home()


@views.route('/lista_assistenti')
@login_required
def mostra_lista_assistenti():
    if not session['isApicoltore']:
        assistenti = get_assistenti()
        return render_template('lista_assistenti.html', assistenti=assistenti)
    return home()

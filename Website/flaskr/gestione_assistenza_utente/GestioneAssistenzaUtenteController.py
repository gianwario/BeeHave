from flask import Blueprint, request, flash, session

from Website.flaskr.Routes import crea_area_assistenza_page, area_personale, mostra_lista_assistenti
from Website.flaskr.gestione_assistenza_utente.GestioneAssistenzaUtenteService import inserisci_area_assistenza, \
    get_assistenti

gau = Blueprint('gau', __name__)


@gau.route('/crea_area_assistenza', methods=['GET', 'POST'])
def crea_area_assistenza():
    if request.method == 'POST' and session['isApicoltore']:
        descrizione = request.form.get('descrizione')
        assistenza = bool(request.form.get('assistenza'))
        if not 0 < len(descrizione) < 200:
            flash('La lunghezza della descrizione non è valida!', category='error')
            return crea_area_assistenza_page()

        inserisci_area_assistenza(descrizione, assistenza)

    return area_personale()


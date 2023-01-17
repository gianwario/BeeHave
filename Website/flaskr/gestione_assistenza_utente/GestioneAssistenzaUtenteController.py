from flask import Blueprint, request, session
from flask_login import login_required, current_user

from Website.flaskr.Routes import crea_area_assistenza_page, area_personale, richiesta_assistenza_page, \
    visualizza_richieste_assistenza
from Website.flaskr.gestione_assistenza_utente.GestioneAssistenzaUtenteService import inserisci_area_assistenza, \
    richiedi_assistenza

gau = Blueprint('gau', __name__)


@gau.route('/crea_area_assistenza', methods=['GET', 'POST'])
@login_required
def crea_area_assistenza():
    if request.method == 'POST' and session['isApicoltore']:
        descrizione = request.form.get('descrizione')
        if inserisci_area_assistenza(descrizione):
            current_user.descrizione = descrizione
            current_user.assistenza = True
        else:
            return crea_area_assistenza_page()
    return area_personale()


@gau.route('/richiesta_assistenza', methods=['GET', 'POST'])
@login_required
def richiesta_assistenza():
    if request.method == 'POST' and not session['isApicoltore']:
        nome = request.form.get('nome')
        descrizione = request.form.get('descrizione')
        id_apicoltore = request.form.get('id_apicoltore')

        if richiedi_assistenza(nome, descrizione, id_apicoltore):
            return visualizza_richieste_assistenza()

    return richiesta_assistenza_page()

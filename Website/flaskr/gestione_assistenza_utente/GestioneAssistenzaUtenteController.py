from flask import Blueprint, request, flash, session, render_template
from flask_login import login_required, current_user

from Website.flaskr.Routes import crea_area_assistenza_page, area_personale, home, richiesta_assistenza_page
from Website.flaskr.gestione_assistenza_utente.GestioneAssistenzaUtenteService import inserisci_area_assistenza, \
    controlla_apicoltore, richiedi_assistenza, get_ticket_assistenza_by_apicoltore, get_ticket_assistenza_by_cliente

gau = Blueprint('gau', __name__)


@gau.route('/crea_area_assistenza', methods=['GET', 'POST'])
@login_required
def crea_area_assistenza():
    if request.method == 'POST' and session['isApicoltore']:
        descrizione = request.form.get('descrizione')
        assistenza = bool(request.form.get('assistenza'))
        if not 0 < len(descrizione) <= 200:
            flash('La lunghezza della descrizione non è valida!', category='error')
            return crea_area_assistenza_page()
        current_user.descrizione = descrizione
        current_user.assistenza = assistenza
        inserisci_area_assistenza(descrizione, assistenza)

    return area_personale()


@gau.route('/richiesta_assistenza', methods=['GET', 'POST'])
@login_required
def richiesta_assistenza():
    if request.method == 'POST' and not session['isApicoltore']:
        nome = request.form.get('nome')
        descrizione = request.form.get('descrizione')
        id_apicoltore = request.form.get('id_apicoltore')

        if not 0 < len(nome) <= 45:
            flash('La lunghezza del nome non è valida', category='error')
            return richiesta_assistenza_page()
        if not 0 < len(descrizione) <= 200:
            flash('La lunghezza della descrizione non è valida!', category='error')
            return richiesta_assistenza_page()
        if not controlla_apicoltore(id_apicoltore):
            flash("L'apicoltore non esiste o non è disponibile a fornire assistenza", category='error')
            return richiesta_assistenza_page()

        richiedi_assistenza(nome, descrizione, id_apicoltore)
        return home()

    return richiesta_assistenza_page()


@gau.route('/visualizza_richieste_assistenza', methods=['POST', 'GET'])
@login_required
def visualizza_richieste_assistenza():
    if session['isApicoltore']:
        ticket_assistenza = get_ticket_assistenza_by_apicoltore(current_user.id)
        return render_template('/ticket_assistenza.html', ticket_assistenza_ap=ticket_assistenza)
    else:
        ticket_assistenza = get_ticket_assistenza_by_cliente(current_user.id)
        return render_template('/ticket_assistenza.html', ticket_assistenza_cl=ticket_assistenza)



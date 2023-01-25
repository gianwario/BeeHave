import smtplib
from email.message import EmailMessage

from flask import Blueprint, request, session
from flask_login import login_required, current_user

from Website.flaskr.Routes import mostra_alveari, modifica_stato, home, informazioni_alveare, inserimento_alveare_page
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import inserisci_alveare, adozione_alveare, \
    aggiorna_stato, get_alveare_by_id
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_id, get_cliente_by_id

ga = Blueprint('ga', __name__)
email_sender = 'beehaveofficial@gmail.com'
email_password = "wqvjngkoeuuafctd"
em = EmailMessage()


@ga.route('/inserimento_alveare', methods=['GET', 'POST'])
@login_required
def inserimento_alveare():
    if request.method == 'POST' and session['isApicoltore']:
        nome = request.form.get('nome')
        produzione = request.form.get('produzione')
        numero_api = request.form.get('numero_api')
        tipo_miele = request.form.get('tipo_miele')
        tipo_fiore = request.form.get('tipo_fiore')
        prezzo = request.form.get('prezzo')

        if not inserisci_alveare(nome=nome, produzione=produzione, numero_api=numero_api, tipo_miele=tipo_miele,
                                 prezzo=prezzo, tipo_fiore=tipo_fiore, apicoltore=current_user):
            return inserimento_alveare_page()

    return mostra_alveari()


@ga.route('/modifica_stato_alveare', methods=['GET', 'POST'])
@login_required
def modifica_stato_alveare():
    if request.method == 'POST' and session['isApicoltore']:
        covata_compatta = request.form.get('covata_compatta')
        popolazione = request.form.get('popolazione')
        polline = request.form.get('polline')
        stato_cellette = request.form.get('stato_cellette')
        stato_larve = request.form.get('stato_larve')
        alveare_id = request.form.get('alveare_id')
        alveare = get_alveare_by_id(alveare_id)
        if alveare is not None:
            if aggiorna_stato(alveare, covata_compatta, popolazione, polline, stato_cellette, stato_larve):
                return informazioni_alveare(alveare_id)
        return modifica_stato(alveare_id)
    return home()


@ga.route('/adotta_alveare/<int:id_apicoltore>/<int:id_cliente>', methods=['POST', 'GET'])
@login_required
def adotta_alveare(id_apicoltore, id_cliente):
    if request.method == 'POST' and not session['isApicoltore']:
        tempo_adozione = request.form.get('tempo_adozione')
        percentuale = request.form.get('disp')
        id_alveare = request.form.get('id_alv')
        alveare = get_alveare_by_id(id_alveare)
        apicoltore = get_apicoltore_by_id(id_apicoltore)
        cliente = get_cliente_by_id(id_cliente)
        prezzo = str(alveare.prezzo)

        if alveare is not None:
            adozione_alveare(percentuale=percentuale, tempo_adozione=tempo_adozione, alveare=alveare,
                             cliente=current_user)
            subject = 'Alveare adottato!'
            body = ('Ciao ' + apicoltore.nome + ',\nIl tuo alveare "' + alveare.nome + '" è stato adottato per il' +
                    percentuale + '%\n I dati dell\'acquirente sono:\n' + cliente.nome + ", "
                    + cliente.cognome + "\n" + cliente.email + "\n" + cliente.telefono +
                    "\n\nTi invitiamo a contattare il Cliente per accordarvi sulle modalità di pagamento.")

            em['From'] = email_sender
            em['To'] = apicoltore.email
            em['Subject'] = subject
            em.set_content(body)

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.connect("smtp.gmail.com", 587)

            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, apicoltore.email, em.as_string())

            smtp.quit()
            em.clear()
            """
                Email Cliente              
            """
            subject_client = 'Alveare adottato con successo!'
            body_client = ('Grazie per l\'acquisto!\nEcco un resoconto della tua adozione di "' + alveare.nome
                           + ":\nPrezzo: " + prezzo + " €\nPercentuale: " + percentuale
                           + "%\nTempo: " + tempo_adozione
                           + " mesi\n\n Acquistato da: " + apicoltore.nome + "(" + apicoltore.email + ")" +
                           "\n Grazie per aver supportato questo apicoltore e le sue api!")
            em['From'] = email_sender
            em['To'] = cliente.email
            em['Subject'] = subject_client
            em.set_content(body_client)

            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.connect("smtp.gmail.com", 587)

            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, cliente.email, em.as_string())

            smtp.quit()
            em.clear()

            return informazioni_alveare(id_alveare)
    return mostra_alveari()

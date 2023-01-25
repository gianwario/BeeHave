import smtplib
from email.message import EmailMessage

from flask import Blueprint, request, session
from flask_login import current_user, login_required

from Website.flaskr.Routes import mostra_prodotti, mostra_articoli_in_vendita, info_articolo, inserimento_prodotto_page
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_id, get_cliente_by_id
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, cancella_prodotto, \
    acquisto_prodotto, get_prodotto_by_id

gv = Blueprint('gv', __name__)

email_sender = 'beehaveofficial@gmail.com'
email_password = "aosryhipaiuafdev"
em = EmailMessage()


@gv.route('/inserimento_prodotto', methods=['GET', 'POST'])
@login_required
def inserimento_prodotto():
    if request.method == 'POST' and session['isApicoltore']:
        nome = request.form.get('nome')
        descrizione = request.form.get('descrizione')
        localita = request.form.get('localita')
        peso = request.form.get('peso')
        tipologia = request.form.get('tipologia')
        prezzo = request.form.get('prezzo')
        quantita = request.form.get('quantita')
        if not inserisci_prodotto(nome, descrizione, localita, peso, tipologia, prezzo, quantita, current_user):
            return inserimento_prodotto_page()
    return mostra_articoli_in_vendita(current_user.id)


@gv.route('/elimina_prodotto', methods=['POST', 'GET'])
@login_required
def elimina_prodotto():
    if request.method == 'POST' and session['isApicoltore']:
        id_apicoltore = request.form.get("id_apicoltore")
        if id_apicoltore != current_user.id:
            id_prodotto = request.form.get("id_prodotto")
            cancella_prodotto(id_prodotto)
    return mostra_articoli_in_vendita(current_user.id)


@gv.route('/acquista_prodotto/<int:id_apicoltore>/<int:id_cliente>', methods=['POST', 'GET'])
@login_required
def acquista_prodotto(id_apicoltore, id_cliente):
    if request.method == 'POST' and not session['isApicoltore']:
        quantita = request.form.get('quantita_prod')
        id_prodotto = request.form.get('id_prd')
        prodotto = get_prodotto_by_id(int(id_prodotto))
        id_apicoltore = prodotto.id_apicoltore
        apicoltore = get_apicoltore_by_id(id_apicoltore)
        cliente = get_cliente_by_id(current_user.id)
        prezzo = str(prodotto.prezzo)
        totale = float(quantita) * float(prezzo)

        if acquisto_prodotto(id_prodotto=id_prodotto, quantita=quantita, cliente=current_user):
            if not session['isApicoltore']:
                subject = 'Prodotto venduto!'
                body = ('Ciao ' + apicoltore.nome + ',\nIl tuo articolo "' + prodotto.nome + '" è stato venduto.\n'
                        'I dati dell\'acquirente sono:\n' + cliente.nome + ", " + cliente.cognome + "\n" + cliente.email
                        + "\n" + cliente.telefono + "\n\nTi invitiamo a contattare il Cliente per accordarvi "
                                                    "sulle modalità di pagamento.")
                invia_email(subject, body, apicoltore.email)
                """
                    Email Cliente              
                """
                subject_client = 'Prodotto acquistato!'
                body_client = ('Grazie per l\'acquisto!\nEcco un resoconto del tuo acquisto di ' + prodotto.nome
                               + ":\nPrezzo: " + prezzo + " €\nQuantità: " + quantita + "\nTotale: " + str(totale)
                               + " €\n\n Acquistato da: " + apicoltore.nome + "(" + apicoltore.email + ")" +
                               "\n Grazie per aver supportato questo apicoltore e le sue api!")

                invia_email(subject_client, body_client, cliente.email)
                return info_articolo(id_prodotto)

    return mostra_prodotti()


def invia_email(oggetto, corpo, email):
    email_sender = 'beehaveofficial@gmail.com'
    email_password = "aosryhipaiuafdev"
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['Subject'] = oggetto

    em.set_content(corpo)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.connect("smtp.gmail.com", 587)

    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email, em.as_string())

    smtp.quit()
    em.clear()

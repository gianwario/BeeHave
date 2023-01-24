import smtplib
from email.message import EmailMessage

from flask import Blueprint, request, session
from flask_login import current_user, login_required

from Website.flaskr.Routes import mostra_prodotti, mostra_articoli_in_vendita, info_articolo, inserimento_prodotto_page
from Website.flaskr.gestione_utente.GestioneUtenteService import get_apicoltore_by_id, get_cliente_by_id
from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto, cancella_prodotto, \
    acquisto_prodotto

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

        if acquisto_prodotto(id_prodotto=id_prodotto, quantita=quantita, cliente=current_user):
            if not session['isApicoltore']:
                apicoltore = get_apicoltore_by_id(id_apicoltore)
                subject = 'Acquisto Effettuato!'
                body = "Qualcuno ha comprato la tua merda!"
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
                cliente = get_cliente_by_id(id_cliente)
                body_client = "Hai speso soldi!"
                em['From'] = email_sender
                em['To'] = cliente.email
                em['Subject'] = subject
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

            return info_articolo(id_prodotto)

    return mostra_prodotti()

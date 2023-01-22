from flask import session, flash
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash

from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from .. import db

"""
    caratteri per il controllo del form di registrazione
"""
email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]

"""
    Restituisce un apicoltore data l'email
"""


def get_apicoltore_by_email(email):
    return Apicoltore.query.filter_by(email=email).first()


"""
    Restituisce un apicoltore dato l'id
"""


def get_apicoltore_by_id(id_apicoltore):
    return Apicoltore.query.filter_by(id=id_apicoltore).first()


"""
    Restituisce un cliente dato l'id
"""


def get_cliente_by_id(id_cliente):
    return Cliente.query.filter_by(id=id_cliente).first()


"""
    Restituisce un cliente data l'email
"""


def get_cliente_by_email(email):
    return Cliente.query.filter_by(email=email).first()


"""
    Controlla se l'email è già presente nel database
"""


def controlla_email_esistente(email):
    if Cliente.query.filter_by(email=email).first() or Apicoltore.query.filter_by(email=email).first():
        return False
    else:
        return True


"""
    Gestisce la registrazione dell' utente alla piattaforma
    post: flask::session['isApicoltore']==is_apicoltore
"""


def registra_utente(nome, cognome, indirizzo, citta, cap, telefono, email, password, conferma_password, is_apicoltore):
    if controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
        if not controlla_email_esistente(email):
            flash("Email già esistente", category="error")
        elif controlla_password(password, conferma_password):
            if not isinstance(is_apicoltore, str) or not is_apicoltore.isdigit():
                flash("is_apicoltore non è valido")
            elif int(is_apicoltore):
                user = Apicoltore(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap,
                                  telefono=telefono,
                                  email=email, assistenza=0, password=generate_password_hash(password, method='sha256'))
            else:
                user = Cliente(nome=nome, cognome=cognome, indirizzo=indirizzo, citta=citta, cap=cap,
                               telefono=telefono,
                               email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            session['isApicoltore'] = is_apicoltore
            login_user(user)
            flash('Registrazione avvenuta con successo!', category='success')
            return True
    return False


"""
    Gestisce la modifica dei dati dell' utente
"""


def modifica_profilo_personale(nome, cognome, email, telefono, citta, cap, indirizzo, password, conferma_password):
    if controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
        if not controlla_email_esistente(email) and email != current_user.email:
            flash("Email già esistente", category="error")
            return False
        if password != '' and not controlla_password(password, conferma_password):
            return False
        if session['isApicoltore']:
            utente = get_apicoltore_by_id(current_user.id)
        else:
            utente = get_cliente_by_id(current_user.id)

        current_user.nome = utente.nome = nome
        current_user.cognome = utente.cognome = cognome
        current_user.email = utente.email = email
        current_user.telefono = utente.telefono = telefono
        current_user.citta = utente.citta = citta
        current_user.cap = utente.cap = cap
        current_user.indirizzo = utente.indirizzo = indirizzo
        if password != '':
            current_user.password = utente.password = generate_password_hash(password, method='sha256')

        db.session.commit()
        flash('Modifica dati avvenuta con successo!', category='success')
        return True
    return False


"""
    Effettua il controllo dei campi del form della registrazione
"""


def controlla_campi(nome, cognome, indirizzo, citta, cap, telefono, email):
    if not isinstance(nome, str) or not 0 < len(nome) <= 45:
        flash("Nome non valido", category="error")
    elif not isinstance(cognome, str) or not 0 < len(cognome) <= 45:
        flash("Cognome non valido", category="error")
    elif not isinstance(indirizzo, str) or not 0 < len(indirizzo) <= 50:
        flash("Indirizzo non valido", category="error")
    elif not isinstance(citta, str) or not 0 < len(citta) <= 45:
        flash("Città non valida", category="error")
    elif not isinstance(cap, str) or not 0 < len(cap) <= 5 or not cap.isdigit():
        flash("CAP non valido", category="error")
    elif not isinstance(telefono, str) or not 0 < len(telefono) <= 10 or not telefono.isdigit():
        flash("Numero telefono non valido", category="error")
    elif not isinstance(email, str) or not 0 < len(email) <= 45:
        flash("Email non valida", category="error")
    else:
        return True
    return False


"""
    Effettua il controllo della password nel form di registrazione
"""


def controlla_password(password, conferma_password):
    if not isinstance(password, str) or len(password) < 8:
        flash("Lunghezza password deve essere almeno 8 caratteri.", category="error")
    elif not (controllo_caratteri_speciali(password) and controllo_numeri(password)):
        flash("Inserire nel campo password almeno un carattere speciale ed un numero.", category="error")
    elif password != conferma_password:
        flash("Password e Conferma Password non combaciano.", category="error")
    else:
        return True
    return False


"""
    Effettua il controllo dei caratteri speciali della password nel form di registrazione
"""


def controllo_caratteri_speciali(password):
    for char in password:
        for symbol in spec:
            if char == symbol:
                return True
    return False


"""
    Effettua il controllo dei numeri della password nel form di registrazione
"""


def controllo_numeri(password):
    for char in password:
        if char.isdigit():
            return True
    return False

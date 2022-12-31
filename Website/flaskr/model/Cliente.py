from .UtenteRegistrato import UtenteRegistrato
from .. import db
from .Acquisto import Acquisto
from .TicketAdozione import TicketAdozione
from .TicketAssistenza import TicketAssistenza


class Cliente(UtenteRegistrato):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_assistenza = db.relationship('TicketAssistenza', backref='cliente', lazy=True)
    ticket_adozione = db.relationship('TicketAdozione', backref='cliente', lazy=True)
    acquisto = db.relationship('Acquisto', backref='cliente', lazy=True)

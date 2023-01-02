from .UtenteRegistrato import UtenteRegistrato
from .. import db
from .Alveare import Alveare
from .TicketAssistenza import TicketAssistenza
from .Prodotto import Prodotto


class Apicoltore(UtenteRegistrato):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descrizione = db.Column(db.String(200), nullable=True)
    assistenza = db.Column(db.Boolean, nullable=False)
    alveare = db.relationship('Alveare', backref='apicoltore', lazy=True)
    prodotto = db.relationship('Prodotto', backref='apicoltore', lazy=True)
    ticket_assistenza = db.relationship('TicketAssistenza', backref='apicoltore', lazy=True)

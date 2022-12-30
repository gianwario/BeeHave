from flask_login import UserMixin

from .. import db
from .Alveare import Alveare
from .TicketAssistenza import TicketAssistenza
from .Prodotto import Prodotto


class Apicoltore(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   email = db.Column(db.String(45), unique=True, nullable=False)
   password = db.Column(db.String(300),nullable=False)
   nome = db.Column(db.String(45),nullable=False)
   cognome = db.Column(db.String(45), nullable=False)
   indirizzo = db.Column(db.String(50), nullable=False)
   citta = db.Column(db.String(45), nullable=False)
   cap = db.Column(db.Integer, nullable=False)
   telefono = db.Column(db.String(10),nullable=False)
   citta = db.Column(db.String(200), nullable=False)
   assistenza = db.Column(db.Boolean, nullable=False)
   alveare = db.relationship('Alveare', backref='apicoltore', lazy=True)
   prodotto = db.relationship('Prodotto', backref='apicoltore', lazy=True)
   ticket_assistenza = db.relationship('TicketAssistenza', backref='apicoltore', lazy=True)
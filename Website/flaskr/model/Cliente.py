from Website.flaskr import db
from flask_login import UserMixin
class Cliente(db.Model, UserMixin):
   email = db.Column(db.String(45), primary_key=True)
   password = db.Column(db.String(300),nullable=False)
   nome = db.Column(db.String(45),nullable=False)
   cognome = db.Column(db.String(45), nullable=False)
   indirizzo = db.Column(db.String(50), nullable=False)
   citta = db.Column(db.String(45), nullable=False)
   cap = db.Column(db.Integer, nullable=False)
   telefono = db.Column(db.String(10),nullable=False)
   ticket_assistenza = db.relationship('TicketAssistenza', backref='cliente', lazy=True)
   ticket_adozione = db.relationship('TicketAdozione', backref='cliente', lazy=True)
   acquisto = db.relationship('Acquisto', backref='cliente', lazy=True)
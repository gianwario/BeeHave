from .. import db
from .TicketAdozione import TicketAdozione


class Alveare(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    tipo_fiore = db.Column(db.String(30), nullable=False)
    prezzo = db.Column(db.Float, nullable=False)
    produzione = db.Column(db.Integer, nullable=False)
    numero_api = db.Column(db.Integer, nullable=False)
    tipo_miele = db.Column(db.String(30), nullable=False)
    percentuale_disponibile = db.Column(db.Integer, nullable=False)
    covata_compatta = db.Column(db.Boolean, nullable=True)
    popolazione = db.Column(db.String(30), nullable=True)
    polline = db.Column(db.String(30), nullable=True)
    stato_cellette = db.Column(db.String(30), nullable=True)
    stato_larve = db.Column(db.String(30), nullable=True)
    id_apicoltore = db.Column(db.Integer, db.ForeignKey('apicoltore.id'), nullable=False)
    ticket_adozione = db.relationship('TicketAdozione', backref='alveare', lazy=True)

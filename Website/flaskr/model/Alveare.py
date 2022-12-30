from .. import db
from .TicketAdozione import TicketAdozione

class Alveare(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    img_path = db.Column(db.String(200), nullable=False)
    tipo_fiore = db.Column(db.String(45), nullable=False)
    produzione = db.Column(db.Integer, nullable=False)
    numero_api = db.Column(db.Integer, nullable=False)
    tipo_miele = db.Column(db.String(100), nullable=False)
    percentuale_disponibile = db.Column(db.Integer, nullable=False)
    covata_compatta = db.Column(db.Boolean, nullable=False)
    tipo_fiore = db.Column(db.String(30), nullable=False)
    popolazione = db.Column(db.String(30), nullable=False)
    polline = db.Column(db.String(30), nullable=False)
    stato_cellette = db.Column(db.String(30), nullable=False)
    id_apicoltore = db.Column(db.Integer, db.ForeignKey('apicoltore.id'), nullable=False)
    ticket_adozione = db.relationship('TicketAdozione', backref='alveare', lazy=True)
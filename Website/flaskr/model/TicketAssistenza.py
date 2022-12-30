from .. import db
from sqlalchemy.sql import func


class TicketAssistenza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), primary_key=True)
    id_apicoltore = db.Column(db.Integer, db.ForeignKey('apicoltore.id'), primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    descrizione = db.Column(db.String(200), nullable=False)
    data_inizio = db.Column(db.DateTime(timezone=True),default=func.now(), nullable=False)
    data_archiviazione = db.Column(db.DateTime(timezone=True))
    stato = db.Column(db.String(45), nullable=False)

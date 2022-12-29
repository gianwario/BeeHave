from .. import db
from sqlalchemy.sql import func


class TicketAssistenza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(45), db.ForeignKey('cliente.email'), primary_key=True)
    apicoltore = db.Column(db.String(45), db.ForeignKey('apicoltore.email'), primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    descrizione = db.Column(db.String(200), nullable=False)
    data_inizio = db.Column(db.DateTime(timezone=True),default=func.now(), nullable=False)
    data_archiviazione = db.Column(db.DateTime(timezone=True))
    stato = db.Column(db.String(45), nullable=False)

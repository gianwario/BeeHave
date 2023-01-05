from .. import db
from sqlalchemy.sql import func


class TicketAdozione(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), primary_key=True)
    id_alveare = db.Column(db.Integer, db.ForeignKey('alveare.id'), primary_key=True)
    percentuale_adozione = db.Column(db.Integer, nullable=False)
    tempo_adozione = db.Column(db.Integer, nullable=False)
    data_inizio_adozione = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=True)

    def data_fine_adozione(self):
        return self.data_inizio_adozione + self.tempo_adozione

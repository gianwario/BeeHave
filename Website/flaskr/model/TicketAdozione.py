from Website.flaskr import db
from sqlalchemy.sql import func

class TicketAdozione(db.Model):
   cliente = db.Column(db.String(45), db.ForeignKey('cliente.email'), primary_key=True)
   id_alveare = db.Column(db.Integer, db.ForeignKey('alveare.id'), primary_key=True)
   percentuale_produzione = db.Column(db.Integer, nullable=False)
   data_inizio_adozione = db.Column(db.Datetime(timezone=True), default=func.now(), nullable=False)

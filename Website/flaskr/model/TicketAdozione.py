from .. import db
from sqlalchemy.sql import func

class TicketAdozione(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   email_cliente = db.Column(db.String(45), db.ForeignKey('cliente.email'), primary_key=True)
   id_alveare = db.Column(db.Integer, db.ForeignKey('alveare.id'), primary_key=True)
   percentuale_produzione = db.Column(db.Integer, nullable=False)
   data_inizio_adozione = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

from .. import db


class Alveare(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(45),nullable=False)
   tipo_fiore = db.Column(db.String(45),nullable=False)
   produzione = db.Column(db.Integer, nullable=False)
   numero_api = db.Column(db.Integer, nullable=False)
   tipo_miele = db.Column(db.String(100), nullable=False)
   percentuale_disponibile = db.Column(db.Integer, nullable=False)
   covata_compatta = db.Column(db.Boolean, nullable=False)
   tipo_fiore = db.Column(db.String(30), nullable=False)
   popolazione = db.Column(db.String(30),nullable=False)
   polline = db.Column(db.String(30),nullable=False)
   stato_cellette = db.Column(db.String(30),nullable=False)
   apicoltore = db.Column(db.String(45), db.ForeignKey('apicoltore.email'))
   ticket_adozione = db.relationship('TicketAdozione', backref='id_alveare', lazy=True)
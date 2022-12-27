from Website.flaskr import db


class TicketAssistenza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(45), db.ForeignKey('cliente.email'), primary_key=True)
    apicoltore = db.Column(db.String(45), db.ForeignKey('apicoltore.email'), primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    descrizione = db.Column(db.String(200), nullable=False)
    data_inizio = db.Column(db.Datetime(timezone=True), nullable=False)
    data_archiviazione = db.Column(db.String(45))
    stato = db.Column(db.String(45), nullable=False)

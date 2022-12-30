from .. import db
from .Acquisto import Acquisto

class Prodotto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45),nullable=False)
    descrizione = db.Column(db.String(200),nullable=False)
    localita = db.Column(db.String(45), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    tipologia = db.Column(db.String(45), nullable=False)
    prezzo = db.Column(db.Float, nullable=False)
    quantita = db.Column(db.Integer, nullable=False)
    email_apicoltore = db.Column(db.String(45), db.ForeignKey('apicoltore.email'), nullable=False)
    acquisto = db.relationship('Acquisto', backref='prodotto', lazy=True)
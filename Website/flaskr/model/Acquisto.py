from .. import db


class Acquisto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), primary_key=True)
    id_prodotto = db.Column(db.Integer, db.ForeignKey('prodotto.id'), primary_key=True)
    quantita = db.Column(db.Integer, nullable=False)
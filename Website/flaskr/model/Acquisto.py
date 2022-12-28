from Website.flaskr import db


class Acquisto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(45), db.ForeignKey('cliente.email'), primary_key=True)
    id_prodotto = db.Column(db.Integer, db.ForeignKey('prodotto.id'), primary_key=True)

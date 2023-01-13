from flask_login import UserMixin

from .. import db


class UtenteRegistrato(db.Model, UserMixin):
    __abstract__ = True
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    img_profilo = db.Column(db.String(300), nullable=True)
    nome = db.Column(db.String(45), nullable=False)
    cognome = db.Column(db.String(45), nullable=False)
    indirizzo = db.Column(db.String(50), nullable=False)
    citta = db.Column(db.String(45), nullable=False)
    cap = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(10), nullable=False)

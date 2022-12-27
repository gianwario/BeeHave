from Website.flaskr import db


class Apicoltore(db.Model):
   email = db.Column(db.String(45), primary_key=True)
   password = db.Column(db.String(300),nullable=False)
   nome = db.Column(db.String(45),nullable=False)
   cognome = db.Column(db.String(45), nullable=False)
   indirizzo = db.Column(db.String(50), nullable=False)
   citta = db.Column(db.String(45), nullable=False)
   cap = db.Column(db.Integer, nullable=False)
   telefono = db.Column(db.String(10),nullable=False)
   citta = db.Column(db.String(200), nullable=False)
   assistenza = db.Column(db.Boolean, nullable=False)
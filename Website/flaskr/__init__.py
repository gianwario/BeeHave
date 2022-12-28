from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists

db=SQLAlchemy()

"""Inizializzazione"""
def create_app():
    app = Flask(__name__)

    """chiave segreta per criptare cookies"""
    app.config['SECRET_KEY'] = 'BEEHAVE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/beehavedb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .model import Cliente, Acquisto, Alveare, Apicoltore, TicketAdozione, TicketAssistenza, Prodotto

    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()

    else:
        with app.app_context():
            db.create_all()

    return app

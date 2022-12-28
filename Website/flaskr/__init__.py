from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()
"""Inizializzazione"""
def create_app():
    app = Flask(__name__)

    """chiave segreta per criptare cookies"""
    app.config['SECRET_KEY'] = 'BEEHAVE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/beehavedb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    create_database()
    db.init_app(app)

    from . import model

    with app.app_context():
        db.create_all()

    return app

def create_database():
    mysql_engine = create_engine('mysql://root:root@localhost')
    existing_databases = mysql_engine.execute("SHOW DATABASES;")
    existing_databases = [d[0] for d in existing_databases]

    if "beehavedb" not in existing_databases:
        mysql_engine.execute("CREATE DATABASE beehavedb")
        print("DATABASE CREATO")


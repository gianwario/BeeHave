from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME= "beehave.db"

"""Inizializzazione"""
def create_app():
    app = Flask(__name__)
    """chiave segreta per criptare cookies"""
    app.config['SECRET_KEY'] = 'BEEHAVE'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
    db.init_app(app)

    from .model import Cliente
    create_database(app)

    return app

def create_database(app):
    db.create_all(app=app)
    print("Create database")
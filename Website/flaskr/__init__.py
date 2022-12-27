from flask import Flask

"""Inizializzazione"""
def create_app():
    app = Flask(__name__)
    """chiave segreta per criptare cookies"""
    app.config['SECRET_KEY'] = 'BEEHAVE'

    return app
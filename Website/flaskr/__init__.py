from flask import Flask, render_template
import os.path


from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists



db = SQLAlchemy()
image_folder_absolute = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.join('static', 'images'))
"""Inizializzazione"""

def create_app():
    app = Flask(__name__)

    """chiave segreta per criptare cookies"""
    app.config['SECRET_KEY'] = 'BEEHAVE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/beehavedb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager(app)

    from .Routes import views
    from .gestione_utente.GestioneUtenteController import gu
    from .gestione_vendita.GestioneVenditaController import gv
    from .gestione_assistenza_utente.GestioneAssistenzaUtenteController import gau

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(gu, url_prefix='/')
    app.register_blueprint(gv, url_prefix='/')
    app.register_blueprint(gau, url_prefix='/')
    from .model import UtenteRegistrato, Cliente, Apicoltore, Alveare, Prodotto, Acquisto, TicketAdozione, TicketAssistenza

    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()

    else:
        with app.app_context():
            db.create_all()

    @login_manager.user_loader
    def user_loader(email):
        utente = Apicoltore.Apicoltore.query.get(email)
        if utente:
            return utente
        else:
            return Cliente.Cliente.query.get(email)

    @app.errorhandler(401)
    def unauthorized_user(e):
        # note that we set the 401 status explicitly
        return render_template('login_page.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('pageerror.html'), 404

    return app

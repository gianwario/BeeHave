from flask import session
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

from Website.flaskr import create_app
from Website.flaskr.Routes import views
from Website.flaskr.model.Alveare import Alveare
from Website.flaskr.model.Apicoltore import Apicoltore


@views.route('/mock_login_apicoltore')
def mock_login_apicoltore():
    user = Apicoltore( nome="nome", cognome="cognome", indirizzo="indirizzo", citta="citta", cap=84345,
                      telefono=4324324362,
                      email="email", assistenza=1, descrizione="descrizione", password="password")
    if not Apicoltore.query.filter_by(email="email").first():
        db.session.add(user)
        db.session.commit()
    login_user(user, remember=True)
    session['isApicoltore'] = True
    return "ok"


db = SQLAlchemy()


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


@pytest.fixture
def mock_alveare():
    return Alveare(nome="nome", produzione=1, numero_api=1, tipo_miele="tipo_miele",
                   percentuale_disponibile=100,
                   prezzo=2, tipo_fiore="tipo_fiore", id_apicoltore=1)


def mock_apicoltore():
    return Apicoltore.query.filter_by(email="email").first()

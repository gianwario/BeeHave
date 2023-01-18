import pytest
from flask import session
from flask_login import login_user

from Website.flaskr import create_app
from Website.flaskr.Routes import views
from Website.flaskr.model.Apicoltore import Apicoltore


@views.route('/mock_login_apicoltore')
def mock_login_apicoltore():
    user = Apicoltore(id=1, nome="nome", cognome="cognome", indirizzo="indirizzo", citta="citta", cap=84345,
                      telefono=4324324362,
                      email="email", assistenza=1, descrizione="descrizione", password="password")
    login_user(user, remember=True)
    session['isApicoltore'] = True
    return "ok"


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app
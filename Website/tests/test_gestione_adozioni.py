import pytest
from flask import session, get_flashed_messages
from flask_login import login_user

from Website.flaskr import create_app
from Website.flaskr.Routes import views
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import aggiorna_stato
from Website.flaskr.model.Alveare import Alveare
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


@pytest.fixture
def mock_alveare():
    return Alveare(nome="nome", produzione=1, numero_api=1, tipo_miele="tipo_miele",
                   percentuale_disponibile=100,
                   prezzo=2, tipo_fiore="tipo_fiore", id_apicoltore=1)


def test_aggiorna_stato_tc_1_1(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = aggiorna_stato(mock_alveare, '', 'SCARSO', 'SCARSO', 'MEDIO', 'MEDIO')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'CovataCompatta non è stata inserita!'


def test_aggiorna_stato_tc_1_2(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = aggiorna_stato(mock_alveare, '1', '', 'OTTIMO', 'MEDIO', 'MEDIO')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza di Popolazione non valida!'


def test_aggiorna_stato_tc_1_3(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = aggiorna_stato(mock_alveare, '1', 'OTTIMO', 'POLLINENONPRESENTEESTATOCELLETTENONINBUONASALUTE', 'MEDIO',
                                'MEDIO')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza di Polline non valida!'


def test_aggiorna_stato_tc_1_4(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = aggiorna_stato(mock_alveare, '1', 'MEDIO', 'SCARSO', '', 'OTTIMO')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza di Stato Cellette non valida!'


def test_aggiorna_stato_tc_1_5(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = aggiorna_stato(mock_alveare, '1', 'OTTIMO', 'SCARSO', 'MEDIO', 'OTTIMISSIMISSIMOLARVEFANTASTICHE')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza di Stato Larve non valida!'


def test_aggiorna_stato_tc_1_6(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = aggiorna_stato(mock_alveare, '0', 'SCARSO', 'SCARSO', 'MEDIO', 'OTTIMO')
        message = get_flashed_messages(category_filter=['success'])
        assert result is True and message[0] == 'Stato alveare aggiornato correttamente'

from flask import get_flashed_messages
from mock import app, mock_alveare, mock_apicoltore
from Website.flaskr.gestione_adozioni.GestioneAdozioniService import aggiorna_stato, inserisci_alveare


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
        result = aggiorna_stato(mock_alveare, '1', 'OTTIMO', 'POLLINENONPRESENTEESTATOCELLETTENONINBUONASALUTE',
                                'MEDIO',
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


def test_inserisci_alveare_tc_2_1(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('', '1000', '2000', 'Miele di Castagno', '31.50', 'Castanea', mock_apicoltore())
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza Nome non valida!'


def test_inserisci_alveare_tc_2_2(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('Miele&Natura', '1000', '2000', 'Miele di Castagno', '31.50', '', mock_apicoltore())
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza di TipoFiore non valida!'


def test_inserisci_alveare_tc_2_3(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('Miele&Natura', '89654', '2000', 'Miele di Castagno', '31.50', 'Castanea',
                                   mock_apicoltore())
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Quantità produzione non è nel range corretto!'


def test_inserisci_alveare_tc_2_4(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('Miele&Natura', '1000', '2000', '', '31.50', 'Castanea', mock_apicoltore())
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza di TipoMiele non valida!'


def test_inserisci_alveare_tc_2_5(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('Miele&Natura', '1000', '875568 ', 'Miele di Castagno', '31.50', 'Castanea',
                                   mock_apicoltore())
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'NumeroApi non è nel range corretto!'


def test_inserisci_alveare_tc_2_6(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('Miele&Natura', '1000', '2000', 'Miele di Castagno', '-12', 'Castanea',
                                   mock_apicoltore())
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Prezzo non è nel range corretto!'


def test_inserisci_alveare_tc_2_7(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_alveare('Miele&Natura', '1000', '2000', 'Miele di Castagno', '31.50', 'Castanea',
                                   mock_apicoltore())
        message = get_flashed_messages(category_filter=['success'])
        assert result is True and message[0] == 'Inserimento avvenuto con successo!'

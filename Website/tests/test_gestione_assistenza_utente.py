from flask import get_flashed_messages

from Website.flaskr.gestione_assistenza_utente.GestioneAssistenzaUtenteService import inserisci_area_assistenza
from Website.tests.mock import mock_apicoltore, mock_app


def test_crea_area_assistenza_tc_5_1(mock_app, mock_apicoltore):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_area_assistenza('', mock_apicoltore)
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'La lunghezza della descrizione non è valida!'


def test_crea_area_assistenza_tc_5_2(mock_app, mock_apicoltore):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_area_assistenza('Allevamento api africane, pulizia arnie', mock_apicoltore)
        message = get_flashed_messages(category_filter=['success'])
        assert result is True and message[0] == 'Messa a disposizione area assistenza avvenuta con successo!'

from flask import get_flashed_messages

from Website.flaskr.gestione_vendita.GestioneVenditaService import inserisci_prodotto
from mock import app, mock_login_apicoltore


def test_inserimento_prodotto_tc_3_1(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro e '
                                    'un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande '
                                    'quali il thé.',
                                    'Sicilia', '250', 'Biologico', '20.00', '10')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza nome non valida!'


def test_inserimento_prodotto_tc_3_2(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi', '', 'Sicilia', '250', 'Biologico', '20,00', '10')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza descrizione non valida!'


def test_inserimento_prodotto_tc_3_3(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro e '
                                    'un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande'
                                    ' quali il thé.',
                                    '', '250', 'Biologico', '20.00', '10')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza località non valida!'


def test_inserimento_prodotto_tc_3_4(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro '
                                    'e un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande'
                                    ' quali il thé.',
                                    'Sicilia', '3000', 'Biologico', '20.00', '10')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Peso non è nel range corretto'


def test_inserimento_prodotto_tc_3_5(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro e'
                                    ' un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande'
                                    ' quali il thé.',
                                    'Sicilia', '250', '', '20.00', '10')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Lunghezza tipologia non valida!'


def test_inserimento_prodotto_tc_3_6(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro e '
                                    'un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande '
                                    'quali il thé.',
                                    'Sicilia', '250', 'Biologico', '', '10')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Prezzo non è nel range corretto!'


def test_inserimento_prodotto_tc_3_7(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro e '
                                    'un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande '
                                    'quali il thé.',
                                    'Sicilia', '250', 'Biologico', '20.00', '')
        message = get_flashed_messages(category_filter=['error'])
        assert result is False and message[0] == 'Quantità non è nel range corretto!'


def test_inserimento_prodotto_tc_3_8(app):
    with app.app_context(), app.test_client() as test_client:
        test_client.get('/mock_login_apicoltore')
        result = inserisci_prodotto('Miele di agrumi',
                                    'Il miele agrumi si caratterizza per un profumo intenso, un colore molto chiaro e'
                                    ' un aroma delicato che lo rendono perfetto per sostituire lo zucchero in bevande'
                                    ' quali il thé.',
                                    'Sicilia', '250', 'Biologico', '20.00', '10')
        message = get_flashed_messages(category_filter=['success'])
        assert result is True and message[0] == 'Inserimento avvenuto con successo!'
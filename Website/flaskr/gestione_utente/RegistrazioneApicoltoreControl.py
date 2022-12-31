import re

from flask import Blueprint, request

app = Blueprint('app', __name__)


@app.route('/registrazione_apicoltore', methods=['GET', 'POST'])
def sigup():
    if request.method == 'POST':
        global spec
        global num
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        indirizzo = request.form.get('indirizzo')
        citta = request.form.get('citta')
        cap = request.form.get('cap')
        telefono = request.form.get('telefono')
        descrizione = request.form.get('descrizione')
        assistenza = request.form.get('assistenza')
        email = request.form.get('email')
        pwd = request.form.get('password')
        cpwd = request.form.get('confirmpassword')
        if not 0 < nome.__len__() < 45:
            print("Nome length has to be at last 30 characters", "error")
            return  # inserire pagine html di errore
        if not 0 < cognome.__len__() < 45:
            print("Cognome length has to be at last 30 characters", "error")
            return  # inserire pagine html di errore
        if not re.fullmatch('^[A-zÀ-ù ‘-] + {2,60}$', indirizzo) or 0 < indirizzo.__len__() < 45:
            print("Indirizzo length has to be at last 30 characters ", "error")
            return  # inserire pagine html di errore
        if not 0 < citta.__len__() < 200:
            print("Città length has to be at last 30 characters", "error")
            return  # inserire pagine html di errore
        if not cap.__len__() >= 5:
            print("cap length has to be at last 5 numbers", "error")
            return  # inserire pagine html di errore
        if not 0 < telefono.__len__() < 10:
            print("Telefono length has to be at last 9 numbers", "error")
            return  # inserire pagine html di errore
        if not 0 < descrizione.__len__() < 200:
            print("Descrizione length has to be at last 200 characters", "error")
            return  # inserire pagine html di errore
        if not re.fullmatch('^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,10}$', email):
            print("Invalid email", "error")
            return  # inserire pagine html di errore
        if not pwd.__len__() < 8:
            print("Password length has to be at least 8 characters", "error")
            return  # inserire pagine html di errore

        if not any(char in spec for char in pwd) and any(char in num for char in pwd):
            return False
        else:
            return True

        if not pwd == cpwd:
            print("Password and confirm password do not match", "error")
            return  # inserire pagine html di errore

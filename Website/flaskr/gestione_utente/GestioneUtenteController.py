from flask import Blueprint, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from GestioneUtenteService import getApicoltoreByEmail, getClienteByEmail
from ..Routes import views


@views.route('/login', methods=['GET', 'POST'])
def login():
    print('ciao')
    if request.method == 'POST':
        apicoltore = request.form.get('utente')
        email = request.form.get('email')
        pwd = request.form.get('password')
        if apicoltore:
            user = getApicoltoreByEmail(email)
        else:
            user = getClienteByEmail(email)
        if user and check_password_hash(user.password, pwd):
            login_user(user, remember=True)
    return redirect(url_for('home.html'))


@views.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home.html'))
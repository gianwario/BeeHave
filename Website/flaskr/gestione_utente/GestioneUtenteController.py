from flask import Blueprint, request, redirect, url_for
from Website.flaskr.model.Apicoltore import Apicoltore
from Website.flaskr.model.Cliente import Cliente
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

app= Blueprint('app', __name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        apicoltore=request.form.get('utente')
        email=request.form.get('email')
        pwd=request.form.get('password')
        if apicoltore:
            user=Apicoltore.query.filter_by(email=email).first()
        else:
            user = Cliente.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, pwd):
            login_user(user, remember=True)
    return redirect(url_for('base.html'))




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('base.html'))
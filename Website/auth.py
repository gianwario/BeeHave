from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("base.html", boolean=True)

def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        psw = request.form.get('psw')
        repeat_psw = request.form.get('psw-ripeti')
        citta = request.form.get('citta')
        address = request.form.get('address')
        numtelefono = request.form.get('numtelefono')



    return render_template("sign_up.html")

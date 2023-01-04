from flaskr import create_app

"""Avvia il server"""

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


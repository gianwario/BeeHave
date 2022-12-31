from Website.flaskr.model.Apicoltore import Apicoltore

def getApicoltoreByEmail(email):
    return Apicoltore.query.filter_by(email=email).first()

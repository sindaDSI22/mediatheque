import datetime
from run import db

class Abonne(db.Document):
    nom = db.StringField(required=True)
    prenom = db.StringField(required=True)
    adresse = db.StringField(required=True)
    date_inscription = db.DateTimeField(default=datetime.datetime.utcnow)
    emprunts_en_cours = db.ListField(db.ReferenceField('Emprunt'))
    historique_emprunts = db.ListField(db.ReferenceField('Emprunt'))

class Documents(db.Document):
    titre = db.StringField(required=True)
    type = db.StringField(required=True, choices=["Livre", "Magazine", "DVD", "CD", "E-book"])
    auteur = db.StringField(required=True)
    date_publication = db.DateTimeField(default=datetime.datetime.utcnow)
    disponible = db.BooleanField(default=True)
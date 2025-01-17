
import datetime
from flask import jsonify, render_template, request

from . import app
from flask.views import MethodView
from bson import ObjectId
from run import mongo

@app.route('/insert_abonnee', methods=['POST'])
def ajouter_abonne():
    data = request.json
    if not all(k in data for k in ["nom", "prenom", "adresse"]):
        return jsonify({"message": "Les champs 'nom', 'prenom' et 'adresse' sont obligatoires"}), 400

    nouvel_abonne = {
        "nom": data["nom"],
        "prenom": data["prenom"],
        "adresse": data["adresse"],
        "date_inscription": datetime.datetime.now().strftime("%Y/%m/%d"),
        "emprunts_en_cours": [],
        "historique_emprunts": []
    }

    result = mongo.db.abonnes.insert_one(nouvel_abonne)

    return jsonify({"message": "Abonné ajouté avec succès", "id": str(result.inserted_id)}), 201

@app.route('/get_abonnes', methods=['GET'])
def get_abonnes():
    abonnes = mongo.db.abonnes.find()
    abonnes = mongo.db.abonnes.find()
    abonnes_list = []
    for abonne in abonnes:
        abonnes_list.append({
            "_id": str(abonne["_id"]),
            "nom": abonne["nom"],
            "prenom": abonne["prenom"],
            "adresse": abonne["adresse"],
            "date_inscription": abonne["date_inscription"]
        })
    return render_template('index.html', abonnes=abonnes_list)
    return jsonify(abonnes_list), 200

@app.route('/update_abonnes/<id_abonne>', methods=['PUT'])
def modifier_abonne(id_abonne):
    data = request.json

    if not ObjectId.is_valid(id_abonne):
        return jsonify({"message": "ID invalide"}), 400

    abonne_id = ObjectId(id_abonne)

    abonne_existant = mongo.db.abonnes.find_one({"_id": abonne_id})
    if not abonne_existant:
        return jsonify({"message": "Abonné non trouvé"}), 404

    update_fields = {}
    if "nom" in data:
        update_fields["nom"] = data["nom"]
    if "prenom" in data:
        update_fields["prenom"] = data["prenom"]
    if "adresse" in data:
        update_fields["adresse"] = data["adresse"]

    if update_fields:
        result = mongo.db.abonnes.update_one(
            {"_id": abonne_id},
            {"$set": update_fields}
        )

        if result.matched_count == 0:
            return jsonify({"message": "Aucune modification effectuée"}), 400

        return jsonify({"message": "Abonné modifié avec succès"}), 200
    else:
        return jsonify({"message": "Aucune donnée à mettre à jour"}), 400

@app.route('/delete_abonnee/<id_abonne>', methods=['DELETE'])
def supprimer_abonne(id_abonne):
    abonne_id = ObjectId(id_abonne)
    result = mongo.db.abonnes.delete_one({"_id": abonne_id})

    if result.deleted_count == 0:
        return jsonify({"message": "Abonné non trouvé"}), 404

    return jsonify({"message": "Abonné supprimé avec succès"}), 200
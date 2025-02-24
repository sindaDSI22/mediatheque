import datetime
from flask import jsonify, render_template, request
from bson import ObjectId
from . import app
from flask.views import MethodView


@app.route('/insert_document', methods=['POST'])
def insert_document():
    data = request.json

    if not all(k in data for k in ["titre", "type", "auteur"]):
        return jsonify({"message": "Les champs 'titre', 'type' et 'auteur' sont obligatoires"}), 400
    from GestionAbonnee.models import Documents
    nouveau_document = Documents(
        titre=data["titre"],
        type=data["type"],
        auteur=data["auteur"],
        date_publication=datetime.datetime.utcnow(),
        disponible=True
    )

    nouveau_document.save()

    return jsonify({"message": "Document ajouté avec succès", "id": str(nouveau_document.id)}), 201

@app.route('/get_documents', methods=['GET'])
def get_documents():
    from GestionAbonnee.models import Documents
    titre = request.args.get('titre', '')
    auteur = request.args.get('auteur', '')
    type_document = request.args.get('type', '')

    query = {}
    if titre:
        query['titre__icontains'] = titre
    if auteur:
        query['auteur__icontains'] = auteur
    if type_document:
        query['type__icontains'] = type_document

    documents = Documents.objects(**query)

    documents_list = []
    for doc in documents:
        documents_list.append({
            "id": str(doc.id),
            "titre": doc.titre,
            "type": doc.type,
            "auteur": doc.auteur,
            "date_publication": doc.date_publication.isoformat(),
            "disponible": doc.disponible
        })

    return render_template('doc.html', documents=documents_list)


@app.route('/update_document/<id_document>', methods=['PUT'])
def modifier_document(id_document):
    data = request.json
    from GestionAbonnee.models import Documents
    document = Documents.objects(id=id_document).first()

    if not document:
        return jsonify({"message": "Document non trouvé"}), 404

    document.update(
        set__titre=data["titre"],
        set__type=data["type"],
        set__auteur=data["auteur"],
        set__disponible=data.get("disponible", document.disponible)
    )

    return jsonify({"message": "Document modifié avec succès"}), 200

@app.route('/delete_document/<id_document>', methods=['DELETE'])
def supprimer_document(id_document):
    from GestionAbonnee.models import Documents
    document = Documents.objects(id=id_document).first()
    if not document:
        return jsonify({"message": "Document non trouvé"}), 404
    from GestionAbonnee.models import Emprunts
    emprunts_abonne = Emprunts.objects(document=document)
    for emprunt in emprunts_abonne:
        emprunt.delete()
    document.delete()

    return jsonify({"message": "Document supprimé avec succès"}), 200

@app.route('/edit_document/<id_document>', methods=['GET'])
def edit_document(id_document):
    from GestionAbonnee.models import Documents
    document = Documents.objects(id=id_document).first()
    if not document:
        return jsonify({"message": "Document non trouvé"}), 404

    return render_template('modification_doc.html', document=document)

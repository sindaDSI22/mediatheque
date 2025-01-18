import pytest
from run import app


@pytest.fixture
def client():
    """Fixture pour initialiser le client Flask pour les tests"""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        yield client


def test_insert_document(client):
    """Test l'ajout d'un nouveau document."""
    data = {
        "titre": "Livre Test",
        "type": "Livre",
        "auteur": "Auteur Test"
    }
    response = client.post('/document/insert_document', json=data)
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'id' in response.json


def test_get_documents(client):
    """Test la récupération de tous les documents."""
    response = client.get('/document/get_documents')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_insert_emprunt(client):
    """Test l'ajout d'un nouvel emprunt."""
    # Créer un abonné et un document d'exemple
    abonne_data = {"nom": "Dupont", "prenom": "Jean", "adresse": "123 Rue Exemple"}
    document_data = {"titre": "Livre Test", "type": "Livre", "auteur": "Auteur Test"}

    abonne_response = client.post('/abonnee/insert_abonnee', json=abonne_data)
    document_response = client.post('/document/insert_document', json=document_data)

    abonne_id = abonne_response.json['id']
    document_id = document_response.json['id']

    emprunt_data = {
        "abonne_id": abonne_id,
        "document_id": document_id,
        "date_retour_prevue": "2025-02-01T00:00:00Z"
    }

    response = client.post('/emprunt/insert_emprunt', json=emprunt_data)
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'id' in response.json


def test_get_emprunts(client):
    """Test la récupération de tous les emprunts."""
    response = client.get('/emprunt/get_emprunts')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_delete_document(client):
    """Test la suppression d'un document."""
    # Créer un document
    document_data = {"titre": "Livre Test", "type": "Livre", "auteur": "Auteur Test"}
    document_response = client.post('/document/insert_document', json=document_data)
    document_id = document_response.json['id']

    response = client.delete(f'/document/delete_document/{document_id}')
    assert response.status_code == 200
    assert 'message' in response.json


def test_delete_emprunt(client):
    """Test la suppression d'un emprunt."""
    # Créer un abonné, un document, et un emprunt
    abonne_data = {"nom": "Dupont", "prenom": "Jean", "adresse": "123 Rue Exemple"}
    document_data = {"titre": "Livre Test", "type": "Livre", "auteur": "Auteur Test"}

    abonne_response = client.post('/abonnee/insert_abonnee', json=abonne_data)
    document_response = client.post('/document/insert_document', json=document_data)

    abonne_id = abonne_response.json['id']
    document_id = document_response.json['id']

    emprunt_data = {
        "abonne_id": abonne_id,
        "document_id": document_id,
        "date_retour_prevue": "2025-02-01T00:00:00Z"
    }

    emprunt_response = client.post('/emprunt/insert_emprunt', json=emprunt_data)
    emprunt_id = emprunt_response.json['id']

    # Supprimer l'emprunt
    response = client.delete(f'/emprunt/delete_emprunt/{emprunt_id}')
    assert response.status_code == 200
    assert 'message' in response.json


def test_get_emprunts_abonne(client):
    """Test la récupération des emprunts d'un abonné."""
    abonne_data = {"nom": "Dupont", "prenom": "Jean", "adresse": "123 Rue Exemple"}
    document_data = {"titre": "Livre Test", "type": "Livre", "auteur": "Auteur Test"}

    abonne_response = client.post('/abonnee/insert_abonnee', json=abonne_data)
    document_response = client.post('/document/insert_document', json=document_data)

    abonne_id = abonne_response.json['id']
    document_id = document_response.json['id']

    emprunt_data = {
        "abonne_id": abonne_id,
        "document_id": document_id,
        "date_retour_prevue": "2025-02-01T00:00:00Z"
    }

    client.post('/emprunt/insert_emprunt', json=emprunt_data)

    response = client.get(f'/emprunt/get_emprunts_abonne/{abonne_id}')
    assert response.status_code == 200
    assert isinstance(response.json, list)

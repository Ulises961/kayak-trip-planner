from Resources.user_resource import USER_ENDPOINT
import json, uuid

def test_user_missing_arguments(client):
    new_user_json = {"mail": "test2.user@gmail.com"}
    response = client.post("/api/auth/register", json=new_user_json)
    assert response.status_code == 422  # Should fail due to missing required fields

def test_get_user(client, auth_headers, public_id):
    response = client.get(
        f"{USER_ENDPOINT}/{public_id}",
        headers=auth_headers)
    assert response.status_code == 200
    assert json.loads(response.data)['name'] == "Test User"

def test_user_update_name(client, auth_headers, public_id):
    response = client.get(f"{USER_ENDPOINT}/{public_id}", headers=auth_headers)
    user = json.loads(response.data)
    original_public_id = user["id"]
    user["name"] = "Updated Name"
    
    response = client.post(f"{USER_ENDPOINT}/{public_id}/update", json=user, headers=auth_headers)
    assert response.status_code == 200
    assert json.loads(response.data)['id'] == original_public_id
    assert json.loads(response.data)['name'] == "Updated Name"

def test_update_user(client, auth_headers, public_id):
    response = client.get(f"{USER_ENDPOINT}/{public_id}", headers=auth_headers)
    originalUser = json.loads(response.data)
    
    # Include the password in the update payload
    updatedUser = {
        'id': public_id,
        'mail': "ulises.sosa@gmail.com",
        'name': 'Ulises',
        'surname': 'Sosa',
        'username': originalUser['username'],
        'phone': originalUser['phone'],
        'pwd': 'testPassword6$'  # Include password to avoid NOT NULL constraint
    } 
    response = client.post(f"{USER_ENDPOINT}/{public_id}/update", json=updatedUser, headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == "Ulises"
    assert data['surname'] == "Sosa"
    assert data['mail'] == "ulises.sosa@gmail.com"
    assert data['id'] == originalUser["id"]

def test_delete_user(client, auth_headers, public_id_1):
    response = client.delete(
        f"{USER_ENDPOINT}/{public_id_1}",
        headers=auth_headers)
    assert response.status_code == 200



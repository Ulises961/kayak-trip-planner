from Resources.user_resource import USER_ENDPOINT
from Schemas.user_schema import UserSchema
import json, uuid

NUM_USERS_IN_BASE_DB = 2

def test_user_post(app):
    new_user_json = {
        "mail": "test.user@gmail.com",
        "pwd": "testPassword",
        "phone": "+390123456789",
        "name": "Test User",
        "public_id": str(uuid.uuid4())
    }
    
    response = app.post(USER_ENDPOINT, json=new_user_json)
    assert response.status_code == 201
    
def test_user_extra_arguments(app):
    new_user_json = {
        "mail": "test1.user@gmail.com",
        'pwd': 'pwd',
        'phone': '+391234567899',
        'name': 'Don',
        'surname': 'charles',
        'public_id': str(uuid.uuid4())
    }
    
    response = app.post(f"{USER_ENDPOINT}", json=new_user_json)
    assert response.status_code == 201


def test_user_missing_arguments(app):
    new_user_json = {"mail": "test2.user@gmail.com"}
    response = app.post(f"{USER_ENDPOINT}", json=new_user_json)
    assert response.status_code == 500


def test_get_all_users(app):
    response = app.get(USER_ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == NUM_USERS_IN_BASE_DB


def test_get_user(app):
    response = app.get(
        f"{USER_ENDPOINT}?id={1}")
    assert response.status_code == 200
    assert json.loads(response.data)['name'] == "Test User"

def test_update_user(app):
    response = app.get(f"{USER_ENDPOINT}?id={1}")
    originalUser = json.loads(response.data)
    
    updatedUser = {'id':1, 'mail':"ulises.sosa@gmail.com", 'name': 'Ulises', 'surname':'Sosa'} 
    response = app.put(f"{USER_ENDPOINT}", json=updatedUser)
    assert json.loads(response.data)['name'] == "Ulises"
    assert json.loads(response.data)['surname'] == "Sosa"
    assert json.loads(response.data)['mail'] == "ulises.sosa@gmail.com"
    assert json.loads(response.data)['public_id'] == originalUser["public_id"]
    assert response.status_code == 201

def test_delete_user(app):
    response = app.delete(
        f"{USER_ENDPOINT}?&id={1}")
    assert response.status_code == 200



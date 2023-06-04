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
    
    print(f"\n\nnew_user_json = {new_user_json}")    
    print(f"The post object is of type: {type(new_user_json)}")
    
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

def test_user_update_error(app):
    response = app.get(f"{USER_ENDPOINT}?id={1}")
    original_user = json.loads(response.data)
    original_user["name"] = "test"
    
    print(f"\n\noriginal_user = {original_user}")
    print(f"The result of GET is of type: {type(original_user)}")
    
    updated_json = json.dumps(original_user)
    print(f"\njson.dumps(original_user) = {updated_json}")
    print(f"If we do a json.dumps() of the GET we get the type: {type(updated_json)}")
    
    updated_user = json.loads(updated_json)
    print(f"\njson.loads(updated_json) = {updated_user}")
    print(f"If we  then do a json.loads() of the json we get the type: {type(updated_user)}")
    
    print(f"The thing is, non of these are acceppted by the Schema file")    
    
    
    response = app.put(f"{USER_ENDPOINT}", json=updated_user)
    assert json.loads(response.data)['public_id'] == original_user["public_id"]
    assert json.loads(response.data)['name'] == "test"
    assert response.status_code == 201

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



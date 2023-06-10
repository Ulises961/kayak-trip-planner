from Resources.log_resource import LOG_ENDPOINT
from Resources.user_resource import USER_ENDPOINT
import json, uuid 

def create_user(app, id, mail, phone):
    return {
        "id": id,
        "mail": mail,
        "pwd": "testPassword",
        "phone": phone,
        "name": "Test User",
        "public_id": str(uuid.uuid4())
    }

def test_insert_log(app):
    user= create_user(app, 71, "user70@mail.com", "+397777777")
    log = {"id": 70, "hours": 7, "avg_sea": 7, "user_id": 71}

    app.post(USER_ENDPOINT, json=user)
    response = app.post(LOG_ENDPOINT, json=log)
    assert response.status_code == 201
    
def test_insert_extra_log(app):
    user= create_user(app, 71, "user70@mail.com", "+397777777")
    log = {"id": 77, "hours": 7, "avg_sea": 7, "user_id": 71}

    app.post(USER_ENDPOINT, json=user)
    response = app.post(LOG_ENDPOINT, json=log)
    assert response.status_code == 201

def test_update_log(app):
    log = {"id": 70, "hours": 7, "avg_sea": 77, "user_id": 71}
    
    response = app.put(LOG_ENDPOINT, json=log)
    assert json.loads(response.data)['avg_sea'] == 77
    assert response.status_code == 201


def test_get_log_by_id(app):
    response = app.get(f"{LOG_ENDPOINT}?id=70")
    
    assert json.loads(response.data)['avg_sea'] == 77
    assert response.status_code == 200

def test_delete_log(app):
    response = app.delete(f"{LOG_ENDPOINT}?id=70")
    assert response.status_code == 200

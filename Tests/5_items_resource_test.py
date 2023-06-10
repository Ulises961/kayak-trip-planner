from Resources.item_resource import ITEM_ENDPOINT
import json 

def test_insert_item_unchecked(app):
    item = {"id": 55, "category": 'generic', "checked": False, "name": 'generic_item'}

    response = app.post(ITEM_ENDPOINT, json=item)
    assert response.status_code == 201

def test_update_item(app):
    item = {"id": 55, "category": 'generic', "checked": True, "name": 'generic_item'}
    
    response = app.put(ITEM_ENDPOINT, json=item)
    
    assert json.loads(response.data)['checked'] == True
    assert response.status_code == 201


def test_get_item_by_id(app):
    response = app.get(f"{ITEM_ENDPOINT}?id=55")
    assert json.loads(response.data)['checked'] == True
    assert response.status_code == 200

def test_delete_item(app):
    response = app.delete(f"{ITEM_ENDPOINT}?id=55")
    assert response.status_code == 200

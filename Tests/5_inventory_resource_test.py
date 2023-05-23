from Resources.inventory_resource import INVENTORY_ENDPOINT
import json 

def test_insert_inventory_without_trip(app):
    inventory_items = [{"category": 'travel', "name": 'compass'}, {"category": "first_aid", "name": 'scissors'}]
    inventory = {"id": 40 ,"items": inventory_items}

    response = app.post(INVENTORY_ENDPOINT, json=inventory)
    assert response.status_code == 201

def test_update_inventory(app):
    inventory_items = [{"category": 'travel', "name": 'map'}, {"category": "first_aid", "name": 'Oki'}]
    inventory = {"id": 40 ,"items": inventory_items}
    
    response = app.put(INVENTORY_ENDPOINT, json=inventory)
    
    assert json.loads(response.data)['items'][0]['name'] == "map"
    assert json.loads(response.data)['items'][1]['name'] == "Oki"
    assert response.status_code == 201


def test_get_inventory_by_id(app):
    response = app.get(f"{INVENTORY_ENDPOINT}?id=40")
    assert json.loads(response.data)['items'][0]['name'] == "map"
    assert json.loads(response.data)['items'][1]['name'] == "Oki"
    assert response.status_code == 200

def test_delete_inventory(app):
    response = app.delete(f"{INVENTORY_ENDPOINT}?id=40")
    assert response.status_code == 200

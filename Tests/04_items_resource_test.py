from Resources.item_resource import ITEM_ENDPOINT
import json 


def test_update_item(client, auth_headers, user_id, inventory_with_items):
    # Create item first
    item = {"category": 'generic', "checked": False, "name": 'generic_item'}
    item_id =  inventory_with_items['items'][0]['id']
    item['id'] = item_id
    response = client.post(f"{ITEM_ENDPOINT}/{item_id}/update", json=item, headers=auth_headers)
    
    assert response.status_code == 200   

    response = client.get(f"{ITEM_ENDPOINT}/{item_id}", headers=auth_headers)

    assert response.status_code == 200   
    updated_item = json.loads(response.data)
    assert updated_item['category'] == "generic"
    assert updated_item['checked'] == False
    assert updated_item['name'] == "generic_item"


def test_get_item_by_id(client, auth_headers, inventory_with_items):
    item_id =  inventory_with_items['items'][0]['id']
    response = client.get(f"{ITEM_ENDPOINT}/{item_id}", headers=auth_headers)

    assert response.status_code == 200
    assert json.loads(response.data)['name'] == "compass"
    assert json.loads(response.data)['category'] == "travel"
    assert json.loads(response.data)['id'] == item_id


def test_delete_item(client, auth_headers, inventory_with_items):
    item_id =  inventory_with_items['items'][0]['id']
    response = client.delete(f"{ITEM_ENDPOINT}/{item_id}", headers=auth_headers)
    assert response.status_code == 200

from Resources.inventory_resource import INVENTORY_ENDPOINT
import pytest
import json 


@pytest.fixture
def inventory_with_items(client, auth_headers, public_id):
    """Create an inventory with items for testing"""
    inventory_items = [
        {"category": 'travel', "name": 'compass'}, 
        {"category": "first_aid", "name": 'scissors'}
    ]
    inventory = {"items": inventory_items}
    response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    assert response.status_code == 201
    inventory_data = json.loads(response.data)
    
    yield inventory_data
    
    # Cleanup: try to delete the inventory
    try:
        client.delete(f"{INVENTORY_ENDPOINT}/{inventory_data['id']}", headers=auth_headers)
    except:
        pass


@pytest.fixture
def empty_inventory(client, auth_headers, public_id):
    """Create an empty inventory for testing"""
    inventory = {"items": []}
    response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    assert response.status_code == 201
    inventory_data = json.loads(response.data)
    
    yield inventory_data
    
    # Cleanup: try to delete the inventory
    try:
        client.delete(f"{INVENTORY_ENDPOINT}/{inventory_data['id']}", headers=auth_headers)
    except:
        pass


def test_create_inventory_with_items(client, auth_headers, public_id):
    """Test creating an inventory with items"""
    inventory_items = [
        {"category": 'travel', "name": 'compass'}, 
        {"category": "first_aid", "name": 'scissors'}
    ]
    inventory = {"items": inventory_items}

    response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['user_id'] == public_id
    assert len(data['items']) == 2
    assert data['items'][0]['name'] == 'compass'
    assert data['items'][1]['name'] == 'scissors'
    
    # Cleanup
    client.delete(f"{INVENTORY_ENDPOINT}/{data['id']}", headers=auth_headers)

    
def test_create_inventory_empty(client, auth_headers, public_id):
    """Test creating an empty inventory"""
    inventory = {"items": []}

    response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['user_id'] == public_id
    assert len(data['items']) == 0
    
    # Cleanup
    client.delete(f"{INVENTORY_ENDPOINT}/{data['id']}", headers=auth_headers)


def test_get_inventory_by_id(client, auth_headers, inventory_with_items):
    """Test retrieving an inventory by ID"""
    inventory_id = inventory_with_items['id']
    
    response = client.get(f"{INVENTORY_ENDPOINT}/{inventory_id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['id'] == inventory_id
    assert len(data['items']) == 2
    assert data['items'][0]['name'] == 'compass'
    assert data['items'][1]['name'] == 'scissors'


def test_get_all_inventories(client, auth_headers, inventory_with_items, empty_inventory):
    """Test retrieving all inventories for current user"""
    response = client.get(f"{INVENTORY_ENDPOINT}/all", headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2  # At least the two fixtures


def test_update_inventory(client, auth_headers, inventory_with_items):
    """Test updating an inventory"""
    inventory_id = inventory_with_items['id']
    updated_items = [
        {"category": 'travel', "name": 'map'}, 
        {"category": "first_aid", "name": 'Oki'}
    ]
    update_data = {"id": inventory_id, "items": updated_items}
    
    response = client.post(f"{INVENTORY_ENDPOINT}/{inventory_id}/update", headers=auth_headers, json=update_data)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['items'][0]['name'] == "map"
    assert data['items'][1]['name'] == "Oki"


def test_delete_inventory(client, auth_headers, public_id):
    """Test deleting an inventory"""
    # Create an inventory to delete
    inventory = {"items": []}
    create_response = client.post(f"{INVENTORY_ENDPOINT}/create", headers=auth_headers, json=inventory)
    inventory_id = json.loads(create_response.data)['id']
    
    # Delete it
    response = client.delete(f"{INVENTORY_ENDPOINT}/{inventory_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"{INVENTORY_ENDPOINT}/{inventory_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_get_nonexistent_inventory(client, auth_headers):
    """Test retrieving an inventory that doesn't exist"""
    response = client.get(f"{INVENTORY_ENDPOINT}/99999", headers=auth_headers)
    assert response.status_code == 404

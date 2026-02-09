from Resources.log_resource import LOG_ENDPOINT
import pytest
import json


@pytest.fixture
def test_log(client, auth_headers, public_id):
    """Create a test log for testing"""
    log = {"hours": 7, "avg_sea": 5, "user_id": public_id}
    response = client.post(f"{LOG_ENDPOINT}/create", headers=auth_headers, json=log)
    assert response.status_code == 201
    log_data = json.loads(response.data)
    
    yield log_data
    
    # Cleanup: try to delete the log
    try:
        client.delete(f"{LOG_ENDPOINT}/{log_data['id']}", headers=auth_headers)
    except:
        pass


def test_create_log(client, auth_headers):
    """Test creating a new log"""
    log = {"hours": 10, "avg_sea": 3}
    response = client.post(f"{LOG_ENDPOINT}/create", headers=auth_headers, json=log)
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['hours'] == 10
    assert data['avg_sea'] == 3
    assert 'id' in data
    
    # Cleanup
    client.delete(f"{LOG_ENDPOINT}/{data['id']}", headers=auth_headers)


def test_get_all_logs(client, auth_headers, test_log):
    """Test retrieving all logs for current user"""
    response = client.get(f"{LOG_ENDPOINT}/all", headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the test_log fixture


def test_get_endorsed_logs(client, auth_headers):
    """Test retrieving endorsed logs"""
    response = client.get(f"{LOG_ENDPOINT}/endorsed", headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_update_log(client, auth_headers, test_log):
    """Test updating an existing log"""
    log_id = test_log['id']
    updated_data = {"hours": 15, "avg_sea": 8}
    
    response = client.post(f"{LOG_ENDPOINT}/{log_id}/update", headers=auth_headers, json=updated_data)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['hours'] == 15
    assert data['avg_sea'] == 8


def test_delete_log(client, auth_headers, ):
    """Test deleting a log"""
    # Create a log to delete
    log = {"hours": 5, "avg_sea": 2}
    create_response = client.post(f"{LOG_ENDPOINT}/create", headers=auth_headers, json=log)
    log_id = json.loads(create_response.data)['id']
    
    # Delete it
    response = client.delete(f"{LOG_ENDPOINT}/{log_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify deletion by checking all logs
    get_response = client.get(f"{LOG_ENDPOINT}/all", headers=auth_headers)
    data = json.loads(get_response.data)
    log_ids = [log['id'] for log in data]
    assert log_id not in log_ids

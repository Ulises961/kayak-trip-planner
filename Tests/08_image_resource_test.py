"""
Image Resource Tests - Testing image manipulation through parent resources (User and Point).

These tests verify that images can be properly managed through their parent resources
rather than directly, ensuring proper ownership and relationship handling.
"""

import pytest
from Resources.user_resource import USER_ENDPOINT
from Resources.point_resource import POINT_ENDPOINT
import json


# ============================================================================
# User Profile Picture Tests
# ============================================================================

def test_add_profile_picture_to_user(client, auth_headers, public_id):
    """Test adding a profile picture to a user through user endpoint."""
    user_data = {
        "image": {
            "size": 2.5,
            "name": "profile_photo.jpg",
            "location": "/public/images/user/1/profile_pictures"
        }
    }
    
    response = client.post(
        f"{USER_ENDPOINT}/{public_id}/update",
        headers=auth_headers,
        json=user_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['image'] is not None
    assert response_data['image']['name'] == 'profile_photo.jpg'
    assert response_data['image']['size'] == 2.5
    assert response_data['image']['location'] == '/public/images/user/1/profile_pictures'


def test_update_user_profile_picture(client, auth_headers, public_id):
    """Test updating a user's profile picture through user endpoint."""
    # First add a profile picture
    user_data = {
        "image": {
            "size": 3.0,
            "name": "old_profile.png",
            "location": "/public/images/user/1/profile_pictures"
        }
    }
    client.post(f"{USER_ENDPOINT}/{public_id}/update", headers=auth_headers, json=user_data)
    
    # Now update it
    updated_data = {
        "image": {
            "size": 4.5,
            "name": "new_profile.jpg",
            "location": "/public/images/user/1/profile_pictures"
        }
    }
    
    response = client.post(
        f"{USER_ENDPOINT}/{public_id}/update",
        headers=auth_headers,
        json=updated_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['image']['name'] == 'new_profile.jpg'
    assert response_data['image']['size'] == 4.5


def test_get_user_with_profile_picture(client, auth_headers, public_id):
    """Test retrieving a user's profile picture through user endpoint."""
    # First add a profile picture
    user_data = {
        "image": {
            "size": 1.8,
            "name": "avatar.png",
            "location": "/public/images/user/1/profile_pictures"
        }
    }
    client.post(f"{USER_ENDPOINT}/{public_id}/update", headers=auth_headers, json=user_data)
    
    # Retrieve the user
    response = client.get(f"{USER_ENDPOINT}/{public_id}", headers=auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['image'] is not None
    assert response_data['image']['name'] == 'avatar.png'
    assert response_data['image']['size'] == 1.8


def test_remove_user_profile_picture(client, auth_headers, public_id):
    """Test removing a user's profile picture through user endpoint."""
    # First add a profile picture
    user_data = {
        "image": {
            "size": 2.0,
            "name": "temp_profile.jpg",
            "location": "/public/images/user/1/profile_pictures"
        }
    }
    client.post(f"{USER_ENDPOINT}/{public_id}/update", headers=auth_headers, json=user_data)
    
    # Remove it by setting to None
    updated_data = {"image": None}
    
    response = client.post(
        f"{USER_ENDPOINT}/{public_id}/update",
        headers=auth_headers,
        json=updated_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['image'] is None


# ============================================================================
# Point Images Tests
# ============================================================================

@pytest.fixture(scope="function")
def point_with_day(client, auth_headers, itinerary):
    """Create a point for testing image associations."""
    point_data = {
        "day_id": itinerary['days'][0]['id'],
        "type": "interest",
        "latitude": 45.4642,
        "longitude": 9.1900,
        "notes": "Beautiful scenic point"
    }
    response = client.post(
        f"{POINT_ENDPOINT}/create",
        headers=auth_headers,
        json=point_data
    )
    assert response.status_code == 201
    point = json.loads(response.data)
    
    yield point
    
    # Cleanup
    try:
        client.delete(f"{POINT_ENDPOINT}/{point['id']}", headers=auth_headers)
    except Exception:
        pass


def test_add_single_image_to_point(client, auth_headers, point_with_day, itinerary):
    """Test adding a single image to a point through point endpoint."""
    point_id = point_with_day['id']
    
    update_data = {
        "itinerary_id": itinerary['id'],
        "images": [
            {
                "size": 5.2,
                "name": "scenic_view.jpg",
                "location": "/public/images/points/1/photos"
            }
        ]
    }
    
    response = client.post(
        f"{POINT_ENDPOINT}/{point_id}/update",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data['images']) == 1
    assert response_data['images'][0]['name'] == 'scenic_view.jpg'
    assert response_data['images'][0]['size'] == 5.2


def test_add_multiple_images_to_point(client, auth_headers, point_with_day, itinerary):
    """Test adding multiple images to a point through point endpoint."""
    point_id = point_with_day['id']
    
    update_data = {
        "itinerary_id": itinerary['id'],
        "images": [
            {
                "size": 3.1,
                "name": "photo1.jpg",
                "location": "/public/images/points/1/photos"
            },
            {
                "size": 4.8,
                "name": "photo2.png",
                "location": "/public/images/points/1/photos"
            },
            {
                "size": 2.3,
                "name": "photo3.jpg",
                "location": "/public/images/points/1/photos"
            }
        ]
    }
    
    response = client.post(
        f"{POINT_ENDPOINT}/{point_id}/update",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data['images']) == 3
    image_names = [img['name'] for img in response_data['images']]
    assert 'photo1.jpg' in image_names
    assert 'photo2.png' in image_names
    assert 'photo3.jpg' in image_names


def test_update_point_images(client, auth_headers, point_with_day, itinerary):
    """Test updating images on a point through point endpoint."""
    point_id = point_with_day['id']
    
    # First add some images
    initial_data = {
        "itinerary_id": itinerary['id'],
        "images": [
            {
                "size": 2.0,
                "name": "old_photo.jpg",
                "location": "/public/images/points/1/photos"
            }
        ]
    }
    client.post(f"{POINT_ENDPOINT}/{point_id}/update", headers=auth_headers, json=initial_data)
    
    # Update with new images
    updated_data = {
        "itinerary_id": itinerary['id'],
        "images": [
            {
                "size": 5.5,
                "name": "new_photo1.jpg",
                "location": "/public/images/points/1/photos"
            },
            {
                "size": 3.2,
                "name": "new_photo2.png",
                "location": "/public/images/points/1/photos"
            }
        ]
    }
    
    response = client.post(
        f"{POINT_ENDPOINT}/{point_id}/update",
        headers=auth_headers,
        json=updated_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data['images']) == 2
    image_names = [img['name'] for img in response_data['images']]
    assert 'new_photo1.jpg' in image_names
    assert 'new_photo2.png' in image_names
    assert 'old_photo.jpg' not in image_names


def test_get_point_with_images(client, auth_headers, point_with_day, itinerary):
    """Test retrieving a point with its images through point endpoint."""
    point_id = point_with_day['id']
    
    # First add images
    update_data = {
        "itinerary_id": itinerary['id'],
        "images": [
            {
                "size": 6.7,
                "name": "landscape.jpg",
                "location": "/public/images/points/1/photos"
            }
        ]
    }
    client.post(f"{POINT_ENDPOINT}/{point_id}/update", headers=auth_headers, json=update_data)
    
    # Retrieve the point
    response = client.get(f"{POINT_ENDPOINT}/{point_id}", headers=auth_headers)
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data['images']) == 1
    assert response_data['images'][0]['name'] == 'landscape.jpg'
    assert response_data['images'][0]['size'] == 6.7


def test_remove_all_images_from_point(client, auth_headers, point_with_day, itinerary):
    """Test removing all images from a point through point endpoint."""
    point_id = point_with_day['id']
    
    # First add images
    initial_data = {
        "itinerary_id": itinerary['id'],
        "images": [
            {
                "size": 4.0,
                "name": "temp_photo.jpg",
                "location": "/public/images/points/1/photos"
            }
        ]
    }
    client.post(f"{POINT_ENDPOINT}/{point_id}/update", headers=auth_headers, json=initial_data)
    
    # Remove all images
    updated_data = {
        "itinerary_id": itinerary['id'],
        "images": []
    }
    
    response = client.post(
        f"{POINT_ENDPOINT}/{point_id}/update",
        headers=auth_headers,
        json=updated_data
    )
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data['images']) == 0


def test_point_deleted_removes_images(client, auth_headers, point_with_day):
    """Test that deleting a point properly handles its associated images."""
    point_id = point_with_day['id']
    
    # Delete the point
    response = client.delete(f"{POINT_ENDPOINT}/{point_id}", headers=auth_headers)
    
    assert response.status_code == 200
    
    # Verify point is gone
    get_response = client.get(f"{POINT_ENDPOINT}/{point_id}", headers=auth_headers)
    assert get_response.status_code == 404

from Resources.image_resource import IMAGE_ENDPOINT
from Resources.user_resource import USER_ENDPOINT
from Resources.point_resource import POINT_ENDPOINT
import json


def test_insert_profile_picture(app):
    image = {"size": 55, "name": "user.jpeg",
             "location": '/public/images/user/1/profile_pictures'}
    response = app.post(IMAGE_ENDPOINT, json=image)
    assert response.status_code == 201


def test_update_image(app):
    image = {"id": 1, "size": 55, "name": "user.png",
             "location": '/public/images/user/1/profile_pictures'}

    response = app.put(IMAGE_ENDPOINT, json=image)

    assert json.loads(response.data)['name'] == 'user.png'
    assert response.status_code == 201


def test_get_image_by_id(app):
    response = app.get(f"{IMAGE_ENDPOINT}?id=1")
    assert json.loads(response.data)['name'] == 'user.png'
    assert response.status_code == 200


def test_insert_image_to_user(app):
    response = app.get(f"{IMAGE_ENDPOINT}?id=1")
    image = json.loads(response.data)
    user = {
        'id': 2,
        "image": image
    }
    response = app.put(USER_ENDPOINT, json=user)

    assert image['id'] == 1
    assert response.status_code == 201
    assert json.loads(response.data)['image']['id'] == 1
    assert json.loads(response.data)['image']['name'] == 'user.png'
    assert json.loads(response.data)['name'] == 'Don'


def test_delete_image(app):
    response_deletion = app.delete(f"{IMAGE_ENDPOINT}?id=1")
    response_retrieval = app.get(f"{IMAGE_ENDPOINT}?id=1")
    response_user = app.get(f"{USER_ENDPOINT}?id=2")
    user = json.loads(response_user.data)
    assert response_retrieval.status_code == 404
    assert response_deletion.status_code == 200
    assert user['image'] == None
    assert user['name'] == 'Don'


def test_insert_image(app):
    image = {"size": 55, "name": "photo_stop_1",
             "location": '/public/images/user/1/pictures'}
    response = app.post(IMAGE_ENDPOINT, json=image)
    assert response.status_code == 201


def test_associate_to_item(app):
    response_retrieval = app.get(f"{IMAGE_ENDPOINT}?id=2")
    image = json.loads(response_retrieval.data)
    point = {
        'id': 1,
        'images': [{'id': 2}]

    }
    response_update = app.put(f"{POINT_ENDPOINT}", json=point)
    assert image['id'] == 2
    assert response_update.status_code == 201
    assert json.loads(response_update.data)['images'] == [{"id":2, "size": 55.0, "name": "photo_stop_1",
                                                           "location": '/public/images/user/1/pictures'}]

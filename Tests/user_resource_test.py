from Resources.user_resource import USER_ENDPOINT


NUM_PLAYERS_IN_BASE_DB = 4


def test_users_post(app):
    new_user_json = {
        "mail": "test.user@gmail.com", 
        "pwd":"testPassword",
        "phone": "+390123456789",
        "name": "Test User"
        }
    response = app.post(USER_ENDPOINT, json=new_user_json)
    assert response.status_code == 201


# def test_players_post_error(client):
#     missing_pos_json = {"mail": "test.user@gmail.com", 'pwd'}
#     response = client.post(f"{USER_ENDPOINT}", json=missing_pos_json)
#     assert response.status_code == 500


# def test_get_all_players(client):
#     response = client.get(f"{USER_ENDPOINT}")
#     assert response.status_code == 200
#     assert len(response.json) == NUM_PLAYERS_IN_BASE_DB


# def test_get_all_players_by_position(client):
#     response = client.get(f"{USER_ENDPOINT}?position=QB")

#     for player in response.json:
#         assert player["position"] == "QB"


# def test_get_single_player(client):
#     response = client.get("/api/players/1")

#     assert response.status_code == 200
#     assert response.json["name"] == "Alvin Kamara"


# def test_get_single_player_not_found(client):
#     response = client.get("/api/players/16")
#     assert response.status_code == 404

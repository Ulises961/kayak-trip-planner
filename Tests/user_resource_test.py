from Resources.user_resource import USER_ENDPOINT


NUM_PLAYERS_IN_BASE_DB = 2


def test_user_post(app):
    new_user_json = {
        "mail": "test.user@gmail.com", 
        "pwd":"testPassword",
        "phone": "+390123456789",
        "name": "Test User"
        }
    response = app.post(USER_ENDPOINT, json=new_user_json)
    assert response.status_code == 201 

def test_user_extra_arguments(app):
    missing_pos_json = {"mail": "test1.user@gmail.com", 'pwd':'pwd','phone':'+391234567899','name':'Don', 'surname':'charles'}
    response = app.post(f"{USER_ENDPOINT}", json=missing_pos_json)
    assert response.status_code == 201

def test_user_missing_arguments(app):
    missing_pos_json = {"mail": "test2.user@gmail.com"}
    response = app.post(f"{USER_ENDPOINT}", json=missing_pos_json)
    assert response.status_code == 500

def test_get_all_users(app):
    response = app.get(f"{USER_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == NUM_PLAYERS_IN_BASE_DB


# def test_get_all_players_by_position(app):
#     response = app.get(f"{USER_ENDPOINT}?position=QB")

#     for player in response.json:
#         assert player["position"] == "QB"


# def test_get_single_player(app):
#     response = app.get("/api/players/1")

#     assert response.status_code == 200
#     assert response.json["name"] == "Alvin Kamara"


# def test_get_single_player_not_found(app):
#     response = app.get("/api/players/16")
#     assert response.status_code == 404

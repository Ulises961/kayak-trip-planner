import Resources.authentication_resource as auth
from Models.user import User
import json, uuid


def test_auth_token_is_valid(app):
    test_user = User.query.order_by(User.id).first()
    
    token = auth.generate_auth_token(test_user.public_id)
    data = auth.decode_auth_token(token)
    current_user = User.query.filter_by(public_id=data['public_id']).first()

    assert current_user != None
    assert current_user.public_id == test_user.public_id
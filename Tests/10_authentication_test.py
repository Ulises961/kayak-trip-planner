import Resources.authentication_resource as auth
from flask import current_app
from Models.user import User
import jwt, datetime
import pytest

from jwt import ExpiredSignatureError

def generate_invalid_token(public_id):
    return jwt.encode(
        {
            "public_id": public_id,
            "exp": datetime.datetime.utcnow() - datetime.timedelta(minutes=45),
        },
        current_app.config["SECRET_KEY"],
        "HS256",
    )
    

def test_auth_token_is_valid(app):
    test_user = User.query.order_by(User.id).first()
    
    token = auth.generate_auth_token(test_user.public_id)
    data = auth.decode_auth_token(token)
    current_user = User.query.filter_by(public_id=data['public_id']).first()

    assert current_user != None
    assert current_user.public_id == test_user.public_id
    
    
def test_invalid_auth_token(app):
    test_user = User.query.order_by(User.id).first()
    token_data = None
    
    with pytest.raises(ExpiredSignatureError) as info:
        
        token = generate_invalid_token(test_user.public_id)
        token_data = auth.decode_auth_token(token)
    
    assert token_data == None
    
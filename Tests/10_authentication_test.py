import pytest
import jwt
import uuid
import random
from datetime import datetime, timedelta, timezone
from flask import current_app
from http import HTTPStatus

from Models.user import User
from Services.jwt_service import JWTService
from Api.database import db


class TestJWTService:
    """Test JWT token generation and validation"""
    
    def test_generate_access_token(self, app):
        """Test access token generation"""
        user_id = "test-uuid-123"
        email = "test@example.com"
        is_admin = False
        
        token = JWTService.generate_access_token(user_id, email, is_admin)
        
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify payload
        payload = JWTService.decode_token(token)
        assert payload['user_id'] == user_id
        assert payload['email'] == email
        assert payload['is_admin'] == is_admin
        assert payload['token_type'] == 'access'
        assert 'exp' in payload
        assert 'iat' in payload
    
    def test_generate_refresh_token(self, app):
        """Test refresh token generation"""
        user_id = "test-uuid-456"
        
        token = JWTService.generate_refresh_token(user_id)
        
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify payload
        payload = JWTService.decode_token(token)
        assert payload['user_id'] == user_id
        assert payload['token_type'] == 'refresh'
        assert 'exp' in payload
        assert 'iat' in payload
    
    def test_decode_valid_token(self, app):
        """Test decoding a valid token"""
        user_id = "test-uuid-789"
        email = "decode@example.com"
        
        token = JWTService.generate_access_token(user_id, email, False)
        payload = JWTService.decode_token(token)
        
        assert payload['user_id'] == user_id
        assert payload['email'] == email
    
    def test_decode_expired_token(self, app):
        """Test decoding an expired token raises ValueError"""
        # Create expired token
        payload = {
            'user_id': 'expired-user',
            'email': 'expired@example.com',
            'is_admin': False,
            'token_type': 'access',
            'iat': datetime.now(timezone.utc) - timedelta(hours=2),
            'exp': datetime.now(timezone.utc) - timedelta(hours=1)
        }
        
        secret_key = current_app.config['JWT_SECRET_KEY']
        expired_token = jwt.encode(payload, secret_key, algorithm='HS256')
        
        with pytest.raises(ValueError, match="Token has expired"):
            JWTService.decode_token(expired_token)
    
    def test_decode_invalid_token(self, app):
        """Test decoding an invalid token raises ValueError"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(ValueError, match="Invalid token"):
            JWTService.decode_token(invalid_token)
    
    def test_verify_token_correct_type(self, app):
        """Test verifying token with correct type"""
        user_id = "verify-user"
        token = JWTService.generate_access_token(user_id, "verify@test.com", False)
        
        payload = JWTService.verify_token(token, 'access')
        
        assert payload is not None
        assert payload['user_id'] == user_id
        assert payload['token_type'] == 'access'
    
    def test_verify_token_wrong_type(self, app):
        """Test verifying token with wrong type returns None"""
        user_id = "wrong-type-user"
        access_token = JWTService.generate_access_token(user_id, "wrong@test.com", False)
        
        # Try to verify access token as refresh token
        payload = JWTService.verify_token(access_token, 'refresh')
        
        assert payload is None
    
    def test_verify_invalid_token(self, app):
        """Test verifying invalid token returns None"""
        payload = JWTService.verify_token("invalid.token", 'access')
        assert payload is None


class TestAuthenticationEndpoints:
    """Test authentication endpoints"""
    
    def test_register_new_user(self, client):
        """Test registering a new user"""
        new_user_data = {
            "username": f"testuser_{uuid.uuid4().hex[:8]}",
            "mail": f"test_{uuid.uuid4().hex[:8]}@example.com",
            "pwd": "SecurePass123!",
            "phone": f"+123456{random.randint(1000, 9999)}",
            "name": "Test",
            "surname": "User"
        }
        
        response = client.post('/api/auth/register', json=new_user_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'access_token' in data
        assert 'refresh_token' in data
        
        # Verify user was created
        user = User.query.filter_by(mail=new_user_data['mail']).first()
        assert user is not None
        assert user.username == new_user_data['username']
        assert user.public_id is not None
    
    def test_register_duplicate_username(self, client):
        """Test registering with existing username fails"""
        # Create first user
        unique_suffix = uuid.uuid4().hex[:8]
        # Generate numeric-only phone suffix
        phone_suffix = str(hash(unique_suffix) % 10000).zfill(4)
        user_data = {
            "username": f"duplicate_{unique_suffix}",
            "mail": f"first_{unique_suffix}@example.com",
            "pwd": "Password123!",
            "phone": f"+987654{phone_suffix}",
            "name": "First"
        }
        
        response1 = client.post('/api/auth/register', json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same username but different email
        duplicate_data = user_data.copy()
        duplicate_data['mail'] = f"second_{unique_suffix}@example.com"
        duplicate_data['phone'] = f"+111111{phone_suffix}"
        
        response2 = client.post('/api/auth/register', json=duplicate_data)
        assert response2.status_code == 400  # IntegrityError handler
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        incomplete_data = {
            "username": "incomplete"
            # Missing mail, pwd, phone, name
        }
        
        response = client.post('/api/auth/register', json=incomplete_data)
        
        # Should fail validation
        assert response.status_code in [400, 422]
    
    def test_login_valid_credentials(self, client):
        """Test login with valid credentials"""
        # First register a user
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "username": f"loginuser_{unique_suffix}",
            "mail": f"login_{unique_suffix}@example.com",
            "pwd": "LoginPass123!",
            "phone": f"+555555{random.randint(1000, 9999)}",
            "name": "Login"
        }
        
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        # Now login
        login_data = {
            "mail": user_data['mail'],
            "username": user_data['username'],
            "pwd": user_data['pwd']
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'access_token' in data
        assert 'refresh_token' in data
        
        # Verify tokens are valid
        access_payload = JWTService.decode_token(data['access_token'])
        assert access_payload['token_type'] == 'access'
        
        refresh_payload = JWTService.decode_token(data['refresh_token'])
        assert refresh_payload['token_type'] == 'refresh'
    
    def test_login_invalid_password(self, client):
        """Test login with wrong password"""
        # Register user
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "username": f"wrongpass_{unique_suffix}",
            "mail": f"wrongpass_{unique_suffix}@example.com",
            "pwd": "CorrectPass123!",
            "phone": f"+666666{random.randint(1000, 9999)}",
            "name": "Wrong"
        }
        
        client.post('/api/auth/register', json=user_data)
        
        # Login with wrong password
        login_data = {
            "mail": user_data['mail'],
            "username": user_data['username'],
            "pwd": "WrongPassword123!"
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['status'] == 'fail'
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {
            "mail": "nonexistent@example.com",
            "username": "nonexistent",
            "pwd": "SomePassword123!"
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 404  # NoResultFound handler
    
    def test_login_missing_body(self, client):
        """Test login with missing request body"""
        response = client.post('/api/auth/login', json=None)
        
        #Flask returns 415 when Content-Type is not application/json
        assert response.status_code in [400, 415]
    
    def test_refresh_token_valid(self, client):
        """Test refreshing access token with valid refresh token"""
        # Register and login
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "username": f"refreshuser_{unique_suffix}",
            "mail": f"refresh_{unique_suffix}@example.com",
            "pwd": "RefreshPass123!",
            "phone": f"+777777{random.randint(1000, 9999)}",
            "name": "Refresh"
        }
        
        login_response = client.post('/api/auth/register', json=user_data)
        tokens = login_response.get_json()
        refresh_token = tokens['refresh_token']
        
        # Use refresh token to get new access token
        response = client.post('/api/auth/refresh', json={
            "refresh_token": refresh_token
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'access_token' in data
        
        # Verify new access token is valid
        new_access_payload = JWTService.decode_token(data['access_token'])
        assert new_access_payload['token_type'] == 'access'
    
    def test_refresh_token_missing(self, client):
        """Test refresh endpoint with missing token"""
        response = client.post('/api/auth/refresh', json={})
        
        assert response.status_code == 400
    
    def test_refresh_with_access_token(self, client):
        """Test refresh endpoint with access token instead of refresh token"""
        # Get tokens
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "username": f"wrongtoken_{unique_suffix}",
            "mail": f"wrongtoken_{unique_suffix}@example.com",
            "pwd": "WrongToken123!",
            "phone": f"+888888{random.randint(1000, 9999)}",
            "name": "Wrong"
        }
        
        login_response = client.post('/api/auth/register', json=user_data)
        tokens = login_response.get_json()
        access_token = tokens['access_token']  # Using wrong token type
        
        # Try to refresh with access token
        response = client.post('/api/auth/refresh', json={
            "refresh_token": access_token
        })
        
        assert response.status_code == 401  # Should fail verification
    
    def test_refresh_with_invalid_token(self, client):
        """Test refresh with completely invalid token"""
        response = client.post('/api/auth/refresh', json={
            "refresh_token": "invalid.token.here"
        })
        
        assert response.status_code == 401
    
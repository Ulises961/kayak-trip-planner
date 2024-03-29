from http import HTTPStatus
from functools import wraps
from flask import request, jsonify
from Models.user import User


def is_admin(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    return user.admin


def authenticate_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response_object, HTTPStatus.FORBIDDEN
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return response_object, HTTPStatus.UNAUTHORIZED
        user = User.query.filter_by(id=resp).first()
        if not (user and user.active and user.admin):
            return response_object, HTTPStatus.UNAUTHORIZED
        return f(user, *args, **kwargs)

    return decorated_function

def authenticate_restful(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return response_object, HTTPStatus.FORBIDDEN
        
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        
        if isinstance(resp, str):
            response_object['message'] = resp
            return response_object, HTTPStatus.UNAUTHORIZED
        
        user = User.query.filter_by(id=resp).first()
        
        if not user or not user.active:
            return response_object, HTTPStatus.UNAUTHORIZED
        
        return f(user, *args, **kwargs)

    return decorated_function

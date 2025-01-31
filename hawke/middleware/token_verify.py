from functools import wraps
from flask import request, jsonify
from token_handler import token_creator
import jwt

def token_verify(function: callable) -> callable:
    @wraps(function)
    def wrapper(*args, **kwargs):
        raw_token = request.headers.get('Authorization')
        uid = request.headers.get('uid')

        if not raw_token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = raw_token.split(' ')[1]
            token_info = jwt.decode(token, key=token_creator.SECRET_KEY, algorithms=['HS256'])
            token_uid = token_info['uid']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        except KeyError as e:
            return jsonify({'message': f'{e} is missing'}), 401
        
        if int(uid) != token_uid:
            return jsonify({'message': 'Token is invalid'}), 401
        
        next_token = token_creator.refresh(token)
        return function(next_token, *args, **kwargs)
    return wrapper
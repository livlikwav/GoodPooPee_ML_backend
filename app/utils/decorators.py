from app.models.ppcam import Ppcam
from flask import request
from app.models.user import User
import functools

def confirm_account(func):
    """
    Confirm user JWT
    
    :Return: func if vaild token, else json string(fail msg)
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # check JWT
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            # Vaild token(get user_id Integer)
            if not isinstance(resp, str):
                return func(*args, **kwargs)
            # Invalid token(get string error msg)
            else: 
                return {
                    'status' : 'Fail',
                    'message' : resp
                }, 401
        else:
            return {
                'status' : 'Fail',
                'message' : 'Request provide a invalid auth token.'
            }, 401

    return decorator


def confirm_device(func):
    """
    Confirm device JWT
    
    :Return: func if vaild token, else json string(fail msg)
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # check JWT
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Ppcam.decode_auth_token(auth_token)
            # Vaild token(get ppcam_id Integer)
            if not isinstance(resp, str):
                return func(*args, **kwargs)
            # Invalid token(get string error msg)
            else: 
                return {
                    'status' : 'Fail',
                    'message' : resp
                }, 401
        else:
            return {
                'status' : 'Fail',
                'message' : 'Request provide a invalid auth token.'
            }, 401

    return decorator
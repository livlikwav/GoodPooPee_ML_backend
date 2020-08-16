from flask import request, abort, jsonify
from app.models.ppcam import Ppcam
from app.models.user import User
import functools

def device_permission_required(func):
    """
    Restrict API to ppcams with the given permission.
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # check remote IP address
        selected_ppcam = Ppcam.query.filter_by(ip_address = request.remote_addr).first()
        if selected_ppcam:
            return func(*args, **kwargs)
        else: # no permission
            abort(403)
    return decorator
    
def confirm_account(func):
    """
    Confirm JWT
    
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
                return jsonify({
                    'status' : 'Fail',
                    'message' : resp
                })
        else:
            return jsonify({
                'status' : 'Fail',
                'message' : 'Request provide a invalid auth token.'
            })

    return decorator
from flask import request, abort
from app.models.ppcam import Ppcam
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
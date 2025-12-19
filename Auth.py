# auth.py
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from models import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if user and user.role == 'admin':
            return fn(*args, **kwargs)
        return {'message': 'Admin access required'}, 403
    return wrapper

from flask import jsonify, g, session
from functools import wraps

# Role middleware
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = session.get('user')
            
            if not user:
                return jsonify({'error': 'unauthorized - please login'}), 401
            
            if user.get('role') != role:
                return jsonify({'error': f'Access denied. {role} role required'}), 403
            g.user = user
            return f(*args, **kwargs)
        return decorated
    return decorator   


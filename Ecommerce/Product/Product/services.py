import jwt
from .settings import SIMPLE_JWT
from functools import wraps
from django.http import JsonResponse

def authenticate_user(view_func):
    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return JsonResponse({
                'status': 'Failed',
                'status_code': 401,
                'message': 'Authentication token is missing',
            })
        try:
            payload = jwt.decode(token, SIMPLE_JWT['SECRET_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'status': 'Failed',
                'status_code': 401,
                'message': 'Token has expired',
            })
        except jwt.InvalidTokenError:
            return JsonResponse({
                'status': 'Failed',
                'status_code': 401,
                'message': 'Invalid token',
            })
        return view_func(view, request, *args, **kwargs)
    return _wrapped_view

def authenticate_staff(view_func):
    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return JsonResponse({
                'status': 'Failed',
                'status_code': 401,
                'message': 'Authentication token is missing',
            })
        try:
            payload = jwt.decode(token, SIMPLE_JWT['SECRET_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'status': 'Failed',
                'status_code': 401,
                'message': 'Token has expired',
            })
        except jwt.InvalidTokenError:
            return JsonResponse({
                'status': 'Failed',
                'status_code': 401,
                'message': 'Invalid token',
            })
        return view_func(view, request, *args, **kwargs)
    return _wrapped_view

# class AuthJWTMiddleware:
#     def __init__(self, request):
#         self.request = request

#     def authenticate(self):
#         token = self.request.headers.get('Authorization')
#         if token is None:
#             return None
#         try:
#             payload = jwt.decode(token, SIMPLE_JWT['SECRET_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
#             return payload
#         except jwt.ExpiredSignatureError:
#             return None
#         except jwt.InvalidTokenError:
#             return None

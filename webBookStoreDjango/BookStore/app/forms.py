
# from django.contrib.auth.models import User
# import re

# def check_username(username):
#     result = {'result': True,
#               'messenger': username}
#     if not re.match(r'^[a-zA-Z]{1}[a-zA-Z0-9_]{4,}$', username):
#         result['result'] = False
#         result['messenger'] = 'Username must start with a letter, and contain only letters, numbers, and underscores.'
    
#     elif User.objects.filter(username=username).exists():
#         result['result'] = False
#         result['messenger'] = 'Username exists!'
#     return result

# def check_email(email):
#     result = {'result': True,
#               'messenger': email}
#     if not email or email=="":
#         result['result'] = False
#         result['messenger'] = 'Email not emtpy!'
#     elif User.objects.filter(email=email).exists():
#         result['result'] = False
#         result['messenger'] = 'Email exists!'
#     return result

# def check_password(password):
#     result = {'result': True,
#               'messenger': password}
#     if len(password) < 8:
#         result['result'] = False
#         result['messenger'] = 'Password must be at least 8 characters long.'
#     elif not any(char.isdigit() for char in password):
#         result['result'] = False
#         result['messenger'] = 'Password must contain at least one digit.'
#     elif not any(char.islower() for char in password):
#         result['result'] = False
#         result['messenger'] ='Password must contain at least one lowercase letter.'
#     elif not any(char.isupper() for char in password):
#         result['result'] = False
#         result['messenger'] ='Password must contain at least one uppercase letter.'
#     return result

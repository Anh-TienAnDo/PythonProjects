# service.py
import re
from user_model.models import User, Account

def check_existing_data(data):
    existing_data = {}

    # Kiểm tra username đã tồn tại chưa
    username = data.get('username')
    if username and Account.objects.filter(username=username).exists():
        existing_data['username'] = f"Username '{username}' đã tồn tại."

    # Kiểm tra email đã tồn tại chưa
    email = data.get('email')
    if email and Account.objects.filter(email=email).exists():
        existing_data['email'] = f"Email '{email}' đã tồn tại."

    # Kiểm tra phone đã tồn tại chưa
    phone = data.get('phone')
    if phone and User.objects.filter(phone=phone).exists():
        existing_data['phone'] = f"Số điện thoại '{phone}' đã tồn tại."

    return existing_data

def check_password(password, confirm_password):
    error = ""
    if not password:
        error = "Password không được để trống."
    elif len(password) < 8:
        error = "Password phải có ít nhất 8 ký tự."
    elif not any(c.isupper() for c in password):
        error = "Password phải chứa ít nhất 1 ký tự in hoa."
    elif not any(c.islower() for c in password):
        error = "Password phải chứa ít nhất 1 ký tự in thường."
    elif not any(c.isdigit() for c in password):
        error = "Password phải chứa ít nhất 1 số."
    elif password != confirm_password:
        error = "Confirm Password phải giống Password."
    return error

def validate_data(data):
    errors = {}

    # Kiểm tra username
    username = data.get('username')
    if not username:
        errors['username'] = "Username không được để trống."
    elif not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', username):
        errors['username'] = "Username phải bắt đầu bằng chữ cái và chỉ chứa chữ cái và số."

    # Kiểm tra email
    email = data.get('email')
    if not email:
        errors['email'] = "Email không được để trống."
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors['email'] = "Email không hợp lệ."

    # Kiểm tra độ dài phone
    phone = data.get('phone')
    if not phone:
        errors['phone'] = "Phone không được để trống."
    elif len(phone) != 10:
        errors['phone'] = "Phone phải có 10 ký tự."

    # Kiểm tra định dạng của fname và lname
    fname = data.get('fname')
    if fname and not re.match(r'^[a-zA-Z0-9\s]+$', fname):
        errors['fname'] = "First name chỉ được chứa ký tự chữ, số và dấu space."

    lname = data.get('lname')
    if lname and not re.match(r'^[a-zA-Z0-9\s]+$', lname):
        errors['lname'] = "Last name chỉ được chứa ký tự chữ, số và dấu space."

    return errors

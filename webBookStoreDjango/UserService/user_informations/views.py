from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from user_model.models import User, Account, NameUser, Address
from user_model.serializers import *
from UserService import service
import jwt, datetime
from UserService.settings import SIMPLE_JWT


# Create your views here.
# Đây là view để cập nhật thông tin người dùng và thay đổi mật khẩu.

# View để cập nhật thông tin người dùng (GET: lấy thông tin, POST: cập nhật thông tin)
@csrf_exempt
def informations(request, id):
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        resp = {'status'     : 'Failed',
                'status_code': '400',
                'message'    : "Not Token"}
        return JsonResponse(resp, status=400)

    try:
        payload = jwt.decode(jwt=token, key=SIMPLE_JWT.get("SIGNING_KEY"), algorithms=[SIMPLE_JWT.get("ALGORITHM")])
    except jwt.ExpiredSignatureError:
        resp = {'status'     : 'Failed',
                'status_code': '400',
                'message'    : "Error Token!"}
        return JsonResponse(resp, status=400)
    
    
    method = request.method
    if method == "GET":
        try:
            # Lấy thông tin người dùng từ ID
            user = User.objects.get(id=id)
            account = user.account
            name_user = user.name_user
            address = user.address
            # Tạo response JSON chứa thông tin người dùng
            resp = {
                'status'     : 'Success',
                'status_code': '200',
                'data'       : {
                    'user'     : UserSerializer(user).data,
                    'account'  : AccountSerializer(account).data,
                    'name_user': NameUserSerializer(name_user).data,
                    'address'  : AddressSerializer(address).data,
                }
            }
            return JsonResponse(resp)
        except User.DoesNotExist:
            resp = {'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : "User does not exist!"}
            return JsonResponse(resp, status=400)
    if method == "POST":
        data = json.loads(request.body)

        # Kiểm tra dữ liệu trước khi cập nhật
        validation_errors = service.validate_data(data)
        if validation_errors:
            return JsonResponse(
                {'status'     : 'Failed',
                 'status_code': '400',
                 'message'    : validation_errors
                 }, status=400)

        try:
            # Lấy thông tin người dùng từ ID
            user = User.objects.get(id=id)
            account = user.account
            name_user = user.name_user
            address = user.address

            # Cập nhật thông tin tài khoản
            account.username = data.get('username')
            account.email = data.get('email')
            account.save()

            # Cập nhật thông tin tên người dùng
            name_user.fname = data.get('fname')
            name_user.lname = data.get('lname')
            name_user.fullname = data.get('lname') + " " + data.get('fname')
            name_user.save()

            # Cập nhật số điện thoại của người dùng
            user.phone = data.get('phone')
            user.save()

            # Cập nhật địa chỉ của người dùng
            if data.get('street') is not None or data.get('street') != "":
                address.street = data.get('street')
            if data.get('district') is not None or data.get('district') != "":
                address.district = data.get('district')
            if data.get('city') is not None or data.get('city') != "":
                address.city = data.get('city')
            address.save()

            # Tạo response JSON chứa thông tin người dùng đã cập nhật
            resp = {
                'status'     : 'Success',
                'status_code': '201',
                'data'       : {
                    'user'     : UserSerializer(user).data,
                    'account'  : AccountSerializer(account).data,
                    'name_user': NameUserSerializer(name_user).data,
                    'address'  : AddressSerializer(address).data,
                }
            }
            return JsonResponse(resp, status=201)
        except Exception as e:
            resp = {'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : f"Failed to update user: {str(e)}"}
            return JsonResponse(resp, status=400)


# View để thay đổi mật khẩu (POST: thay đổi mật khẩu)
@csrf_exempt
def change_password(request, id):
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        resp = {'status'     : 'Failed',
                'status_code': '400',
                'message'    : "Not Token"}
        return JsonResponse(resp, status=400)

    try:
        payload = jwt.decode(jwt=token, key=SIMPLE_JWT.get("SIGNING_KEY"), algorithms=[SIMPLE_JWT.get("ALGORITHM")])
    except jwt.ExpiredSignatureError:
        resp = {'status'     : 'Failed',
                'status_code': '400',
                'message'    : "Error Token!"}
        return JsonResponse(resp, status=400)
    
    method = request.method
    if method == "POST":
        data = json.loads(request.body)
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Kiểm tra tính hợp lệ của mật khẩu mới
        check_password = service.check_password(password, confirm_password)
        if check_password:
            return JsonResponse(
                {'status'     : 'Failed',
                 'status_code': '400',
                 'message'    : check_password,
                 }, status=400)

        # Lấy tài khoản từ ID
        account = Account.objects.get(id=id)
        # Cập nhật mật khẩu mới
        account.set_password(password)
        account.save()

        # Tạo response JSON báo thành công
        resp = {
            'status'     : 'Success',
            'status_code': '201',
            'messenge'   : "Change Password Success.",
        }
        return JsonResponse(resp, status=201)
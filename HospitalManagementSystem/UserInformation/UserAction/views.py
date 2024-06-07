from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView # Import the missing APIView class
from UserModel.models import Person, Account
from UserModel.serializers import PersonSerializer
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect


class PersonViewSet(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get all users successful!',
                'data': response.data,
            }
        )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '201',
                'message': 'Create user successful!',
            }
        )

# get, put, delete by id
class PersonRetrieveUpdateDestroyAPIViewID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "id"
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get user successful!',
                'data': response.data,
            }
        )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Delete user successful!',
            }
        )

class PersonLogin(APIView):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        try:
            # Kiểm tra sự tồn tại của tài khoản với username và password tương ứng
            account = Account.objects.get(username=username)
            if account.check_password(password):
                user = account.person
                # Trả về thông tin của người dùng và tài khoản trong trường hợp đăng nhập thành công
                return Response(
                    {
                        'status'     : 'Success',
                        'status_code': '200',
                        'message'    : 'Login successful!',
                        'data'       :
                            {
                                'user'     : PersonSerializer(user).data,
                            }
                    })
            else:
                return Response({'status': 'Failed', 'status_code': '400', 'message': "Invalid username or password."}, status=400)
        except Account.DoesNotExist:
            # Trả về thông báo lỗi nếu tài khoản không tồn tại hoặc thông tin đăng nhập không chính xác
            return Response({'status': 'Failed', 'status_code': '400', 'message': "Invalid username or password."}, status=400)


from django.http import JsonResponse
from datetime import datetime

class ResponseGenerator:
    @staticmethod
    def success(data=None, message=None):
        return JsonResponse(
            data={
                "data": data,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, 
            status=200
        )
        
    @staticmethod
    def created(data=None, message=None):
        return JsonResponse(
            data={
                "data": data,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, 
            status=201
        )
        
    @staticmethod 
    def deleted(data=None, message=None):
        return JsonResponse(
            data={
                "data": data,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, 
            status=204
        )

    @staticmethod
    def error(data=None, message=None):
        return JsonResponse(
            data={
                "data": data,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, 
            status=400
        )
        
    @staticmethod
    def not_found(data=None, message=None):
        return JsonResponse(
            data={
                "data": data,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, 
            status=404
        )
        
    @staticmethod
    def unauthorized(data=None, message=None):
        return JsonResponse(
            data={
                "data": data,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, 
            status=401
        )

    
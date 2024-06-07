from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from AppointmentModel.models import *
from AppointmentModel.serializers import  *

# Create your views here.
class AppointmentsListCreate(generics.ListCreateAPIView):
    queryset = Appointments.objects.filter(is_active=True)
    serializer_class = AppointmentsSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get all appointment successful!',
                'data': data,
            }
        )

    def create(self, request):
        serializer = AppointmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'Success',
                    'status_code': '201',
                    'message': 'Create appointment successful!',
                }
            )
        return Response(
                {
                    'status': 'Failed',
                    'status_code': '201',
                    'message': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST
            )

class AppointmentsDetail(generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, pk=None):
        try:
            appointment = Appointments.objects.get(pk=pk)
            serializer = AppointmentsSerializer(appointment)
            data = serializer.data
            return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get patient information successful!',
                'data': data,
            }
        )
        except Appointments.DoesNotExist:
            return Response({
                'status': 'Failed',
                'status_code': '404',
                'message': 'Appointment information not found!',
            },status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            appointment = Appointments.objects.get(pk=pk)
            appointment.is_active = False
            appointment.save()
            return Response({'status': 'Success', "message": "Deleted successfully"}, status=status.HTTP_200_OK)
        except Appointments.DoesNotExist:
            return Response({'status': 'Failed', "message": "Not found"}, status=status.HTTP_404_NOT_FOUND)


from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from PatientModel.models import PatientInformation, HistoryMedical
from PatientModel.serializers import PatientInformationSerializer, HistoryMedicalSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# get all patient information, create patient information
class PatientInformationListCreate(generics.ListCreateAPIView):
    queryset = PatientInformation.objects.filter(is_active=True)
    serializer_class = PatientInformationSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get all patient successful!',
                'data': data,
            }
        )

    def create(self, request):
        serializer = PatientInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'Success',
                    'status_code': '201',
                    'message': 'Create user successful!',
                }
            )
        return Response(
                {
                    'status': 'Failed',
                    'status_code': '201',
                    'message': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST
            )

# get, update, delete patient information by id
class PatientInformationDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = PatientInformation.objects.all()
    # serializer_class = PatientInformationSerializer
    # lookup_field = "id"

    def retrieve(self, request, pk=None):
        try:
            patient_information = PatientInformation.objects.get(pk=pk)
            serializer = PatientInformationSerializer(patient_information)
            data = serializer.data
            return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get patient information successful!',
                'data': data,
            }
        )
        except PatientInformation.DoesNotExist:
            return Response({
                'status': 'Failed',
                'status_code': '404',
                'message': 'Patient information not found!',
            },status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            patient_information = PatientInformation.objects.get(pk=pk)
            serializer = PatientInformationSerializer(patient_information, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PatientInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            patient_information = PatientInformation.objects.get(pk=pk)
            patient_information.is_active = False
            patient_information.save()
            return Response({'status': 'Success', "message": "Deleted successfully"}, status=status.HTTP_200_OK)
        except PatientInformation.DoesNotExist:
            return Response({'status': 'Failed', "message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

# get all history medical, create history medical
class HistoryMedicalListCreate(generics.ListCreateAPIView):
    # queryset = HistoryMedical.objects.filter(is_active=True)
    # serializer_class = HistoryMedicalSerializer

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     data = response.data
    #     return Response(
    #         {
    #             'status': 'Success',
    #             'status_code': '200',
    #             'message': 'Get all history medical successful!',
    #             'data': data,
    #         }
    #     )

    def list(self, request, pk=None):
        queryset = HistoryMedical.objects.filter(patient_information__id=pk, is_active=True)
        serializer = HistoryMedicalSerializer(queryset, many=True)
        data = serializer.data
        return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get all history medical successful!',
                'data': data,
            }
        )

    def create(self, request, pk=None):
        data = json.loads(request.body)
        print(data)
        patient_information = PatientInformation.objects.get(id=data.get('patient_information'))
        history_medical = HistoryMedical.objects.create(
            patient_information=patient_information,
            doctor=data.get('doctor'),
            place_of_examination=data.get('place_of_examination'),
            pathology=data.get('pathology'),
            treatment=data.get('treatment'),
            cost=data.get('cost'),
            paymented=data.get('paymented'),
            description=data.get('description'),
            evaluation=data.get('evaluation'),
        )
        if history_medical is not None:
            return Response(
                {
                    'status': 'Success',
                    'status_code': '201',
                    'message': 'Create successful!',
                }
            )
        return Response(
                {
                    'status': 'Failed',
                    'status_code': '201',
                    'message': "Create failed!",
                }, status=status.HTTP_400_BAD_REQUEST
            )

# get, update, delete history medical by id
class HistoryMedicalDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = HistoryMedical.objects.all()
    # serializer_class = HistoryMedicalSerializer

    def retrieve(self, request, pk=None):
        try:
            history_medical = HistoryMedical.objects.get(pk=pk)
            serializer = HistoryMedicalSerializer(history_medical)
            data = serializer.data
            return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get history medical successful!',
                'data': data,
            }
        )
        except HistoryMedical.DoesNotExist:
            return Response({
                'status': 'Failed',
                'status_code': '404',
                'message': 'History medical not found!',
            },status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            history_medical = HistoryMedical.objects.get(pk=pk)
            serializer = HistoryMedicalSerializer(history_medical, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HistoryMedical.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            history_medical = HistoryMedical.objects.get(pk=pk)
            history_medical.is_active = False
            history_medical.save()
            return Response({'status': 'Success', "message": "Deleted successfully"}, status=status.HTTP_200_OK)
        except HistoryMedical.DoesNotExist:
            return Response({'status': 'Failed', "message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

# get all history medical by doctor id
class HistoryMedicalListByDoctor(generics.ListAPIView):
    # @csrf_exempt
    # @staticmethod
    def get(self, request, pk):
        try:
            history_medical = HistoryMedical.objects.filter(doctor=pk, is_active=True)
            serializer = HistoryMedicalSerializer(history_medical, many=True)
            data = serializer.data
            return Response(
            {
                'status': 'Success',
                'status_code': '200',
                'message': 'Get history medical successful!',
                'data': data,
            }
        )
        except HistoryMedical.DoesNotExist:
            return Response({
                'status': 'Failed',
                'status_code': '404',
                'message': 'History medical not found!',
            },status=status.HTTP_404_NOT_FOUND)



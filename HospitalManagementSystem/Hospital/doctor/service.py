import requests
from json import *

class Doctor:
    def __init__(self):
        pass

    def get_doctor(self, url='http://127.0.0.1:9998/doctors/', id=1):
        doctor = requests.get(url + str(id)).json()
        if doctor['status'] == "Failed":
            return False
        doctor = doctor.get('data')
        return doctor
    
    def get_doctors(self, url='http://127.0.0.1:9998/doctors/'):
        doctors = requests.get(url).json()
        if doctors['status'] == "Failed":
            return False
        doctors = doctors.get('data')
        return doctors
    
    def delete_doctor(self, url='http://127.0.0.1:9998/doctors/', id=1):
        doctor = requests.get(url + str(id) + "/delete").json()
        return doctor

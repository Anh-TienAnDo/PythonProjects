import requests
from json import *
from doctor.service import Doctor

class Patient:
    def __init__(self):
        pass

    def get_patient(self, url='http://127.0.0.1:9996/patients/information/', id=1):
        patient = requests.get(url + str(id)).json()
        if patient['status'] == "Failed":
            return False
        patient = patient.get('data')
        return patient
    
    def get_patients(self, url='http://127.0.0.1:9996/patients/information'):
        patients = requests.get(url).json()
        if patients['status'] == "Failed":
            return False
        patients = patients.get('data')
        print(patients)
        return patients
    
    def create_patient(self, url='http://127.0.0.1:9996/patients/information', data={}):
        patient = requests.post(url, json=data).json()
        if patient['status'] == "Failed":
            return False
        return patient

    def delete_patient(self, url='http://127.0.0.1:9996/patients/information/', id=1):
        patient = requests.delete(url + str(id) + '/').json()
        if patient['status'] == "Failed":
            return False
        return patient
    
    def get_history_medical_list(self, url='http://127.0.0.1:9996/patients/', id=1):
        history_medical_list = requests.get(url + str(id) + "/history_medical/").json()
        if history_medical_list['status'] == "Failed":
            return False
        history_medical_list = history_medical_list.get('data')
        return history_medical_list
    
    def get_history_medical(self, url='http://127.0.0.1:9996/patients/history_medical/', id=1):
        history_medical = requests.get(url + str(id)).json()
        if history_medical['status'] == "Failed":
            return False
        history_medical = history_medical.get('data')
        ob_doctor = Doctor()
        doctor = history_medical.get('doctor')
        history_medical['doctor'] = ob_doctor.get_doctor(id=doctor)
        return history_medical
    
    def create_history_medical(self, url='http://127.0.0.1:9996/patients/', id=1, data={}):
        history_medical = requests.post(url + str(id) + "/history_medical", json=data).json()
        if history_medical['status'] == "Failed":
            return False
        return history_medical
    
    def delete_history_medical(self, url='http://127.0.0.1:9996/patients/history_medical/', id=1):
        history_medical = requests.delete(url + str(id) + '/').json()
        if history_medical['status'] == "Failed":
            return False
        return history_medical
    
    def get_history_medical_list_by_doctor(self, url='http://127.0.0.1:9996/patients/history_medical/', id=1):
        history_medical = requests.get(url + str(id) + "/doctor").json()
        if history_medical['status'] == "Failed":
            return False
        history_medical = history_medical.get('data')
        print("history_medical: ", history_medical)
        return history_medical

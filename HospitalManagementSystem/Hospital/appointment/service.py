import requests
from json import *
from doctor.service import Doctor
from patientln.service import Patient

class Appointment:
    def __init__(self):
        pass

    def get_appointment(self, url='http://127.0.0.1:9995/appointments/', id=1):
        appointment = requests.get(url + str(id) + '/').json()
        if appointment['status'] == "Failed":
            return False
        appointment = appointment.get('data')
        ob_patient = Patient()
        ob_doctor = Doctor()
        appointment['patient'] = ob_patient.get_patient(id=appointment.get('patient'))
        appointment['doctor'] = ob_doctor.get_doctor(id=appointment.get('doctor'))
        return appointment
    
    def get_appointments(self, url='http://127.0.0.1:9995/appointments/'):
        appointments = requests.get(url).json()
        if appointments['status'] == "Failed":
            return False
        appointments = appointments.get('data')
        return appointments
    
    def delete_appointment(self, url='http://127.0.0.1:9995/appointments/', id=1):
        appointment = requests.delete(url + str(id) + '/').json()
        if appointment['status'] == "Failed":
            return False
        return appointment
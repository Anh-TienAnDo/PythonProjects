from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .service import Patient

# Service instance
patient_service = Patient()

# List all patients
def patients(request):
    patients = patient_service.get_patients()
    request.session['patients'] = patients
    context = {
        'page_title': 'Patients',
        'patients': patients
    }
    return render(request, 'patientln/patients.html', context=context)

# View patient details
def patient_details(request, pk):
    patient = patient_service.get_patient(id=pk)
    context = {
        'page_title': 'Patient Details',
        'patient': patient
    }
    return render(request, 'patientln/patient_details.html', context=context)

# Create a new patient
def patient_create(request):
    context = {
        'page_title': 'Create Patient',
    }
    if request.method == 'POST':
        pass
    return render(request, 'patientln/patient_form.html', context=context)

# Delete a patient
def patient_delete(request, pk):
    patient_service.delete_patient(id=pk)
    return redirect('patientln:patients')

# List all history medical records for a patient
def patient_history_medical_list(request, pk):
    history_medical_list = patient_service.get_history_medical_list(id=pk)
    context = {
        'page_title': 'History Medical List',
        'history_medical_list': history_medical_list,
        'patient_id': pk
    }
    return render(request, 'patientln/history_medical_list.html', context = context)

# View history medical details
def patient_history_medical_details(request, pk):
    history_medical = patient_service.get_history_medical(id=pk)
    context = {
        'page_title': 'History Medical Details',
        'history_medical': history_medical
    }
    return render(request, 'patientln/history_medical_details.html', context=context)

# Create a new history medical record
def patient_history_medical_create(request, pk):
    context = {
        'page_title': 'Create History Medical',
    }
    if request.method == 'POST':
        pass
    return render(request, 'patientln/history_medical_form.html', context=context)

# Delete a history medical record
def patient_history_medical_delete(request, pk):
    history_medical = patient_service.delete_history_medical(id=pk)
    return redirect(request.META.get('HTTP_REFERER'))

def patient_history_medical_doctor(request, pk):
    history_medical_list = patient_service.get_history_medical_list_by_doctor(id=pk)
    context = {
        'page_title': 'History Medical List',
        'history_medical_list': history_medical_list,
        'doctor_id': pk
    }
    return render(request, 'patientln/history_medical_list.html', context=context)

from django.shortcuts import render, redirect
from .service import Doctor

# Create your views here.
def index(request):
    object = Doctor()
    doctors = object.get_doctors()
    print(doctors)
    context = {
        'page_title': 'Doctors',
        'doctors': doctors
    }
    if 'doctors' not in request.session:
        request.session['doctors'] = doctors
    return render(request, 'doctor/index.html', context=context)

def doctor_details(request, id):
    object = Doctor()
    doctor = object.get_doctor(id=id)
    context = {
        'page_title': 'Doctor Details',
        'doctor': doctor
    }
    return render(request, 'doctor/details.html', context=context)

def delete(request, id):
    object = Doctor()
    doctor = object.delete_doctor(id=id)
    return redirect('doctor:doctors')

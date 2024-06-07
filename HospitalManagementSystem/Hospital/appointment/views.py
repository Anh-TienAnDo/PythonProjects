from django.shortcuts import render, redirect
from .service import Appointment

# Create your views here.
ob_appointment = Appointment()

def appointments(request):
    appointments = ob_appointment.get_appointments()
    request.session['appointments'] = appointments
    context = {
        'page_title': 'Appointments',
        'appointments': appointments
    }
    return render(request, 'appointment/appointments.html', context=context)

def appointment_details(request, pk):
    appointment = ob_appointment.get_appointment(id=pk)
    context = {
        'page_title': 'Appointment Details',
        'appointment': appointment
    }
    return render(request, 'appointment/appointment_details.html', context=context)

def appointment_delete(request, pk):
    appointment.delete_appointment(id=pk)
    return redirect(request.META.get('HTTP_REFERER'))

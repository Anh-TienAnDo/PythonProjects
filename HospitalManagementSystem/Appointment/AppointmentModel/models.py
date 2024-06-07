from django.db import models

# Create your models here.
class Appointments(models.Model):
    doctor = models.IntegerField(default=1)
    patient = models.IntegerField(default=1)
    appointment_date_time = models.DateTimeField(null=True)
    place_of_examination = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for patient {self.patient} with doctor {self.doctor} on {self.appointment_date_time}"

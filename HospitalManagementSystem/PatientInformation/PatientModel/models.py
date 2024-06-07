from djongo import models
from django.utils.text import slugify

class Name(models.Model):
    fname = models.CharField(max_length=255, null=True)
    lname = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.fullname = f"{self.lname} {self.fname}"
        super(Name, self).save(*args, **kwargs)

    def __str__(self):
        return self.fullname

class Address(models.Model):
    street = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.district}, {self.city}"

class PatientInformation(models.Model):
    name = models.OneToOneField(Name, on_delete=models.SET_NULL, null=True)
    day_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=12, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name.fullname} - {self.phone}"


class HistoryMedical(models.Model):
    patient_information = models.ForeignKey(PatientInformation, on_delete=models.CASCADE)
    doctor = models.IntegerField(default=1)
    place_of_examination = models.CharField(max_length=255)
    pathology = models.TextField()
    treatment = models.TextField()
    cost = models.IntegerField(default=100000)
    paymented = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    evaluation = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"History for {self.patient_information.name.fullname} by {self.doctor}"


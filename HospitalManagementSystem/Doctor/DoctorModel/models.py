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

class Specialty(models.Model):
     # each individual status
    TYPE1 = "Khoa Chấn Thương Chỉnh Hình Và CS"
    TYPE2 = 'Khoa Da Liễu'
    TYPE3 = 'Khoa Mắt'
    TYPE4 = 'Khoa Nội tiết'
    TYPE5 = 'Khoa Tai Mũi Họng'
    # set of possible order statuses
    TYPE_STATUSES = ((TYPE1, TYPE1),
                      (TYPE2, TYPE2),
                      (TYPE3, TYPE3),
                      (TYPE4, TYPE4),
                      (TYPE5, TYPE5))
    name = models.CharField(max_length=255, choices=TYPE_STATUSES, default=TYPE1)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Specialty, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Level, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class PlaceWork(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PlaceWork, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.OneToOneField(Name, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=255, null=False)
    image = models.TextField()
    year_of_birth = models.IntegerField(default=0)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=12, null=False)
    specialties = models.ManyToManyField(Specialty)
    level = models.OneToOneField(Level, on_delete=models.SET_NULL, null=True)
    salary = models.IntegerField(default=0)
    place_of_work = models.OneToOneField(PlaceWork, on_delete=models.SET_NULL, null=True)
    year_of_work = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name.fullname} {self.phone}")
        super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name.fullname

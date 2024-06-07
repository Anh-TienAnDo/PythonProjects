from django.db import models

# Create your models here.
class Payment(models.Model):
    bank = models.CharField(max_length=30, null=True)
    checkout = models.BigIntegerField(null=True, blank=True) # one-to-one
    code = models.CharField(max_length=25, null=True)
    total = models.BigIntegerField(null=True)
    paymented = models.BigIntegerField(null=True)
    missing = models.BigIntegerField(null=True)
    completed = models.BooleanField(default=False)
    note = models.TextField()
    date_completed = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.thanh_toan)



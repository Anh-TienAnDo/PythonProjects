from djongo import models
from django.contrib.auth.models import User

class SearchTerm(models.Model):
    query = models.CharField(max_length=50)
    search_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.q

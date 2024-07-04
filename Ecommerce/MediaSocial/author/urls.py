from django.urls import path
from .views import AuthorView

urlpatterns = [
    path('', AuthorView.as_view()),
]
# Compare this snippet from MediaSocial/author/serializers.py:
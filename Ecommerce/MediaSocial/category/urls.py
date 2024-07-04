from django.urls import path
from .views import CategoryView

urlpatterns = [
    path('', CategoryView.as_view()),
]
# Compare this snippet from MediaSocial/category/serializers.py:


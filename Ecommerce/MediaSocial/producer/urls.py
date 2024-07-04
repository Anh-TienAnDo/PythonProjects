from django.urls import path
from .views import ProducerView

urlpatterns = [
    path('', ProducerView.as_view()),
]
# Compare this snippet from MediaSocial/producer/serializers.py:
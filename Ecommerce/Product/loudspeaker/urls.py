from django.urls import path
from .views import LoudspeakerSearchAndFilterView, LoudspeakerFilterView, LoudspeakerView, LoudspeakerDetailView

urlpatterns = [
    # GET /api/.../?_start=0&_limit=12
    path('', LoudspeakerView.as_view()),
    path('detail/<slug:slug>/', LoudspeakerDetailView.as_view()),
    path('search-and-filter/', LoudspeakerSearchAndFilterView.as_view()),
    path('filter/', LoudspeakerFilterView.as_view()),
]
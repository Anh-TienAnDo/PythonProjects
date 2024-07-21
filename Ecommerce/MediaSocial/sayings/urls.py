from django.urls import path
from .views import *
urlpatterns = [
    # GET /api/sayings/?start=0&limit=12
    path('count/', count_sayings),
    path('', SayingView.as_view(), name='saying-list'),
    path('<slug:slug>/', SayingDetailView.as_view(), name='saying-detail'),
    path('category/<slug:category_slug>/', SayingByCategoryView.as_view(), name='saying-by-category'),
    path('author/<slug:author_slug>/', SayingByAuthorView.as_view(), name='saying-by-author'),
    path('category/<slug:category_slug>/author/<slug:author_slug>/', SayingByCategoryAndAuthorView.as_view(), name='saying-by-category-author'),
]

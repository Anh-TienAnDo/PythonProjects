from django.urls import path
from .views import *

urlpatterns = [
    # GET /api/sayings/?start=0&limit=12
    path('', SayingView.as_view(), name='saying-list'),
    path('detail/<slug:slug>/', SayingDetailView.as_view(), name='saying-detail'),
    path('filter/', SayingFilterView.as_view(), name='saying-filter'),
    # GET /api/sayings/?_query=abc&_start=0&_limit=12
    path('search-by-title/', SayingSearchByTitleView.as_view(), name='saying-search-by-title'),
    path('search-by-content/', SayingSearchByContentView.as_view(), name='saying-search-by-content'),
    path('search-by-author/', SayingSearchByAuthorView.as_view(), name='saying-search-by-author'),
    
]

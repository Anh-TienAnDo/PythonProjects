from django.urls import path
from .views import *
urlpatterns = [
    # GET /api/sayings/?start=0&limit=12
    path('', SayingView.as_view(), name='saying-list'),
    path('<slug:slug>/', SayingDetailView.as_view(), name='saying-detail'),
    path('category/<slug:category_slug>/', SayingByCategoryView.as_view(), name='saying-by-category'),
    path('author/<slug:author_slug>/', SayingByAuthorView.as_view(), name='saying-by-author'),
    path('category/<slug:category_slug>/author/<slug:author_slug>/', SayingByCategoryAndAuthorView.as_view(), name='saying-by-category-author'),
    # GET /api/sayings/?_query=abc&_start=0&_limit=12
    path('search-by-title/', SayingSearchByTitleView.as_view(), name='saying-search-by-title'),
    path('search-by-content/', SayingSearchByContentView.as_view(), name='saying-search-by-content'),
    path('search-by-author/', SayingSearchByAuthorView.as_view(), name='saying-search-by-author'),
    
]

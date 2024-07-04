from django.urls import path
from .views import *
urlpatterns = [
    # GET /api/sayings/?start=0&limit=12
    path('count/', count_sayings),
    path('', SayingView.as_view(), name='saying-list'),
    path('<int:id>/', SayingDetailView.as_view(), name='saying-detail'),
    path('category/<int:category_id>/', SayingByCategoryView.as_view(), name='saying-by-category'),
    path('author/<int:author_id>/', SayingByAuthorView.as_view(), name='saying-by-author'),
    path('category/<int:category_id>/author/<int:author_id>/', SayingByCategoryAndAuthorView.as_view(), name='saying-by-category-author'),
]

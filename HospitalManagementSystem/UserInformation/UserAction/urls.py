from .views import *
from django.urls import path, include


urlpatterns = [
    path('', PersonViewSet.as_view()),
    path('<int:id>/', PersonRetrieveUpdateDestroyAPIViewID.as_view()),
    # path('register', PersonRegister.as_view, name="register"),
    path('login/', PersonLogin.as_view(), name="login"),
    # path('uchange-password/<int:id>', views.change_password, name="change-password"),
]
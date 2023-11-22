from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.login),
    path("signup", views.signup),
    path("api/", include("api.urls"))
]

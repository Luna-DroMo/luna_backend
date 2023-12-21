from django.urls import path, include
from . import views

urlpatterns = [
    path("test", views.test),
    path("signup", views.signup),
    path("login", views.login),
    path("api/", include("api.urls"))
]

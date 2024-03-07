from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing),
    path("signup", views.signup),
    path("login", views.login),
    path("api/", include("api.urls"))
]

from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path("login", views.login),
    re_path("signup", views.signup),
    re_path("test_token", views.test_token),
    # all the CRUD operations for student users
    re_path(
        "users/get_all_studentusers",
        views.get_studentusers,
        name="get_all_studentusers",
    ),
    path(
        "users/get_studentuser/<int:pk>/",
        views.get_studentuser,
        name="get_studentuser",
    ),
    path(
        "users/update_studentuser/<int:pk>/",
        views.update_studentuser,
        name="update_studentuser",
    ),
    path(
        "users/delete_studentuser/<int:pk>/",
        views.delete_studentuser,
        name="delete_studentuser",
    ),
    # all the CRUD operations for all users
    re_path("users/get_all_users", views.get_users),
]

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
        "users/update_studentuser_with_PK/<int:pk>/",
        views.update_studentuser_with_PK,
        name="update_studentuser_with_PK",
    ),
    path(
        "users/update_studentuser_with_email/<str:email>/",
        views.update_studentuser_with_email,
        name="update_studentuser_with_email",
    ),
    path(
        "users/delete_studentuser_with_pk/<int:pk>/",
        views.delete_studentuser_with_pk,
        name="delete_studentuser_with_pk",
    ),
    path(
        "users/delete_studentuser_with_email/<str:email>/",
        views.delete_studentuser_with_email,
        name="delete_studentuser_with_email",
    ),
    # all the CRUD operations for all users
    path(
        "users/update_user_with_email/<str:email>/",
        views.update_user_with_email,
        name="update_user_with_email",
    ),
    # path(
    #     "users/delete_user_with_email/<str:email>/",
    #     views.delete_user_with_email,
    #     name="delete_user_with_email",
    # ),
    re_path("users/get_all_users", views.get_users),
]

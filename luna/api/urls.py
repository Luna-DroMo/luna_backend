from django.urls import path
from . import views

urlpatterns = [
    path("hello", views.hello_world, name="hello"),
    path(
        "update_student/<int:pk>/",
        views.update_studentuser_with_id,
        name="update_studentuser_with_PK",
    ),
    path("student/<int:student_id>/modules",
         views.get_student_modules, name="get_student_modules"),
    path("handle_post", views.handle_post, name="handle_post"),
    path(
        "get_all_studentusers",
        views.get_studentusers,
        name="get_all_studentusers",
    ),
    path(
        "student/save_form/<int:student_id>",
        views.save_form, name="save_form_data"
    ),
    path(
        "getUserType/<int:id>",
        views.getUserType,
        name="get_user_type"
    )
]

# urlpatterns = [  # all the CRUD operations for student users
#     path(
#         "users/get_all_studentusers",
#         views.get_studentusers,
#         name="get_all_studentusers",
#     ),
#     path(
#         "users/get_studentuser_with_pk/<int:pk>/",
#         views.get_studentuser_with_pk,
#         name="get_studentuser",
#     ),
#     path(
#         "users/get_studentuser_with_email/<str:email>/",
#         views.get_studentuser_with_email,
#         name="get_studentuser",
#     ),
#     path(
#         "users/update_studentuser_with_PK/<int:pk>/",
#         views.update_studentuser_with_PK,
#         name="update_studentuser_with_PK",
#     ),
#     path(
#         "users/update_studentuser_with_email/<str:email>/",
#         views.update_studentuser_with_email,
#         name="update_studentuser_with_email",
#     ),
#     path(
#         "users/delete_studentuser_with_pk/<int:pk>/",
#         views.delete_studentuser_with_pk,
#         name="delete_studentuser_with_pk",
#     ),
#     path(
#         "users/delete_studentuser_with_email/<str:email>/",
#         views.delete_studentuser_with_email,
#         name="delete_studentuser_with_email",
#     ),
#     # all the CRUD operations for all users
#     path("users/get_all_users", views.get_users),
#     path(
#         "users/get_user_with_email/<str:email>/",
#         views.get_user_with_email,
#         name="get_user_with_email",
#     ),
#     path(
#         "users/update_user_with_email/<str:email>/",
#         views.update_user_with_email,
#         name="update_user_with_email",
#     ),]

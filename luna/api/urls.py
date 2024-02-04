from django.urls import path
from . import views
from .views import TestView
urlpatterns = [
    path("test", TestView.as_view(), name="test"),
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
    ),
    path(
        "createModule",
        views.createModule,
        name="create_module"
    ),
    path(
        "getModuleByID",
        views.get_module_by_id,
        name="get_module_by_id"
    )
]

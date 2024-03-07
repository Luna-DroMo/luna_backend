from django.urls import path
from . import views
from .views import TestView, ModuleView
urlpatterns = [
    path("test", TestView.as_view(), name="test"),
    path(
        "update_student/<int:pk>/",
        views.update_studentuser_with_id,
        name="update_studentuser_with_PK",
    ),
    path("student/<int:student_id>/modules",
         views.get_student_modules, name="get_student_modules"),
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
        "<int:student_id>/info",
        views.StudentView.as_view(), name="get_student_info"
    ),

    path('<int:student_id>/modules',
         ModuleView.as_view(), name='student_modules'),
    path("<int:student_id>/forms", views.StudentFormsView.as_view(),
         name="get_all_student_forms"),
    path("<int:student_id>/forms/<int:form_id>",
         views.StudentFormsView.as_view(), name="handle_student_forms"),
    path("<int:student_id>/background", views.get_background_status,
         name="get_background_status"),

]

from django.urls import path
from . import views

urlpatterns = [
    path(
        "update_student/<int:pk>/",
        views.update_studentuser_with_id,
        name="update_studentuser_with_PK",
    ),
    path(
        "student/<int:student_id>/modules",
        views.get_student_modules,
        name="get_student_modules",
    ),
    path(
        "get_all_studentusers",
        views.get_studentusers,
        name="get_all_studentusers",
    ),
    path("student/save_form/<int:student_id>", views.save_form, name="save_form_data"),
    path("<int:student_id>/info", views.StudentView.as_view(), name="get_student_info"),
    path(
        "<int:student_id>/modules", views.ModuleView.as_view(), name="student_modules"
    ),
    path(
        "<int:student_id>/forms",
        views.StudentFormsView.as_view(),
        name="get_all_student_forms",
    ),
    path(
        "<int:student_id>/forms/<int:form_id>",
        views.StudentFormsView.as_view(),
        name="handle_student_forms",
    ),
    path(
        "<int:student_id>/background",
        views.get_background_status,
        name="get_background_status",
    ),
    path("getUserType/<int:id>", views.getUserType, name="get_user_type"),
    path(
        "<int:student_id>/module/<int:module_id>",
        views.enroll_module,
        name="enroll_module",
    ),
    path(
        "<int:student_id>/modules",
        views.get_student_modules,
        name="get_student_modules",
    ),
    path(
        "<int:student_id>/surveys/<int:survey_id>",
        views.SurveyView.as_view(),
        name="handle_survey",
    ),
    path("<int:student_id>/modules", views.SurveyView.as_view(), name="get_surveys"),
    path(
        "universities",
        views.get_all_universities,
        name="get_universities",
    ),
    path(
        "universities/<int:university_id>",
        views.get_university_faculties,
        name="get_university_faculties",
    ),
    path(
        "lecturer/<int:lecturer_id>/modules",
        views.get_lecturer_modules,
        name="get_lecturer_modules",
    ),
    path("module/<int:module_id>", views.get_module_details, name="get_module_details"),
    path(
        "<int:student_id>/modules/available",
        views.get_available_modules,
        name="get_available_modules",
    ),
    path("<int:user_id>/module/create", views.create_module),
]

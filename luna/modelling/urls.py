from django.urls import path
from . import views

urlpatterns = [
    path("run", views.run, name="run_model"),
    path(
        "results/survey/<int:survey_id>",
        views.get_student_module_modelling_results,
        name="get_student_module_modelling_results",
    ),
]

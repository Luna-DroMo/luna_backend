from django.urls import path
from . import views

urlpatterns = [
    path("run", views.run, name="run_model"),
    path(
        "<int:student_id>/module/<int:module_id>",
        views.get_student_module_modelling_results,
        name="get_student_module_modelling_results",
    ),
    path(
        "module/<int:module_id>",
        views.get_module_modelling_results,
        name="get_module_modelling_results",
    ),
]

from django.urls import path
from .views import run_model

urlpatterns = [path("run_model/", run_model, name="run_model")]

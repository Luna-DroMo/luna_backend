from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model

from .modelling import KalmanFilter
from . import model_settings as MS
import numpy as np
import pandas as pd
from rest_framework.response import Response
from core.models import StudentUser, Module, StudentSurvey
from .models import Results
from django.utils import timezone


@api_view(["POST"])
def run(request):
    student_id = request.data.get("student_id")
    module_id = request.data.get("module_id")
    data = run_model(student_id, module_id)

    return Response({"data": data})

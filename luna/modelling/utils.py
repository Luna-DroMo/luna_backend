from .modelling import KalmanFilter
from . import model_settings as MS
import numpy as np
import pandas as pd
from rest_framework.response import Response
from core.models import StudentUser, Module, StudentSurvey
from .models import Results
from django.utils import timezone


def run_model(student_id, module_id):
    try:
        if not student_id or not module_id:
            return Response({"error": "Missing student_id or module_id"}, status=400)

        student_instance = StudentUser.objects.get(id=student_id)
        module_instance = Module.objects.get(id=module_id)
        survey_number_t = ...
        surveys = StudentSurvey.objects.filter(
            student_id=student_id, module_id=module_id
        )

        # Convert the QuerySet to a list of dictionaries
        survey_data = np.array(list(surveys.values()))  # t x 3

        kalman_filter = KalmanFilter(F=MS.F, H=MS.H, Q=MS.Q, R=MS.R, x0=MS.x0)

        raw_state, predictions_cov, predictions_obs = kalman_filter.forward(
            survey_data  # eg np.array([[2], [3], [1]])
        )
        smooth_state, cov_smooth, K = kalman_filter.rts_smoother(
            np.array(raw_state), np.array(predictions_cov)
        )

        SurveyNumber_T = StudentSurvey.objects.last(
            student_id=student_id, module_id=module_id
        )
        raw_state = raw_state.flatten()
        smooth_state - smooth_state.flatten()

        for raw_state, smooth_state, raw_cov, smooth_cov in zip(
            raw_state, smooth_state, predictions_cov, cov_smooth
        ):
            Results.objects.create(
                student=student_instance,
                module=module_instance,
                smoothed_output=smooth_state,
                raw_output=raw_state,
                covariance_matrix=raw_cov,
                smooth_covariance_matrix=smooth_cov,
                SurveyNumber_T=survey_number_t.id,
                time_evaluated=timezone.now(),
            )
        print("Model run successfully")
        return True
    except Exception as e:
        print(str(e))
        return False

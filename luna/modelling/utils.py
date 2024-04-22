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

        student_instance = StudentUser.objects.get(user=student_id)
        module_instance = Module.objects.get(id=module_id)

        surveys = StudentSurvey.objects.filter(
            student_id=student_id, module_id=module_id
        )

        data = surveys.values_list("content", flat=True)
        print(data)

        survey_data = np.array(list(data))

        print("Student ID, ModuleID", student_id, module_id)
        print("Survey data:", survey_data)

        kalman_filter = KalmanFilter(F=MS.F, H=MS.H, Q=MS.Q, R=MS.R, x0=MS.x0)

        print("BUMBLEBEE: Running model...", survey_data)

        raw_state, predictions_cov, predictions_obs = kalman_filter.forward(
            survey_data  # eg np.array([[2], [3], [1]])
        )

        smooth_state, cov_smooth, K = kalman_filter.smooth(
            np.array(raw_state), np.array(predictions_cov)
        )

        raw_state = np.array(raw_state).flatten()
        smooth_state = np.array(smooth_state).flatten()

        for survey, r_state, s_state, r_cov, s_cov in zip(
            surveys, raw_state, smooth_state, predictions_cov, cov_smooth
        ):
            Results.objects.update_or_create(
                student=student_instance,
                module=module_instance,
                SurveyNumber_T=survey.survey_number,  # Use the survey number directly
                defaults={
                    "smoothed_output": np.array(s_state).flatten().tolist(),
                    "raw_output": np.array(r_state).flatten().tolist(),
                    "covariance_matrix": np.array(r_cov).flatten().tolist(),
                    "smooth_covariance_matrix": np.array(s_cov).flatten().tolist(),
                    "time_evaluated": timezone.now(),
                },
            )
        print("Model run successfully")
        return True
    except Exception as e:
        print(str(e))
        return False

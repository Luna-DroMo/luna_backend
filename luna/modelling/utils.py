from django.http import JsonResponse
from .modelling import KalmanFilter
import numpy as np
import pandas as pd
from rest_framework.response import Response
from core.models import StudentUser, Module, StudentSurvey
from .models import Results
from django.utils import timezone


def run_model(student_id, module_id):
    try:
        # Validate the input
        if not student_id or not module_id:
            return Response({"error": "Missing student_id or module_id"}, status=400)

        student_instance = StudentUser.objects.get(id=student_id)
        module_instance = Module.objects.get(id=module_id)
        survey_number_t = ...
        surveys = StudentSurvey.objects.filter(
            student_id=student_id, module_id=module_id
        )

        # Convert the QuerySet to a list of dictionaries
        survey_data = list(surveys.values())

        data = pd.DataFrame(survey_data)
        kalman_filter = KalmanFilter()

        predictions_state, predictions_cov, predictions_obs = kalman_filter.forward(
            data
        )
        state_smooth, cov_smooth, K = kalman_filter.rts_smoother(
            predictions_state, predictions_cov
        )

        for state, covariance in zip(predictions_state, predictions_cov):
            Results.objects.create(
                student=student_instance,
                module=module_instance,
                smoothed_output=state.tolist(),  # Adjust based on actual mapping
                raw_output=covariance.tolist(),  # Adjust based on actual mapping
                SurveyNumber_T=survey_number_t,
                time_evaluated=timezone.now(),  # This is automatically handled by auto_now_add=True
            )
        print("Model run successfully")
    except Exception as e:
        return Response(print(e))

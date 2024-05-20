from .modelling import KalmanFilter
from . import model_settings as MS
import numpy as np
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
                    "smoothed_output": np.array(s_state).flatten().tolist()[0],
                    "raw_output": np.array(r_state).flatten().tolist()[0],
                    "covariance_matrix": np.array(r_cov).flatten().tolist()[0],
                    "smooth_covariance_matrix": np.array(s_cov).flatten().tolist()[0],
                    "time_evaluated": timezone.now(),
                },
            )
        print("Model run successfully")
        return True
    except Exception as e:
        print(str(e))
        return False




# ------------------------------------------------------------------
# Storing the required matricies for the AIST/PANAS etc questionnaires here



# PANAS
# First Entry relates to PA (postive)
# Second Entry relates to NA (negative)

# This is a 20x2 matrix. Use as follows:
# PANAS response: vector of length 20, or matrix of 1x20
# panas_response @ l_aist -> 1x20 @ 20x2 = 1x2 matrix containing PA and NA measurements
l_panas = np.array([
    [.67, 0], # Attentive / Aufmerksam
    [0, .71], # Nervous / Nervös
    [.70, 0], # Determined / Entschlossen
    [0, .70], # Scared / Erschocken
    [.58, 0], # Proud / Stolz
    [0, .46], # Guilty / Schuldig
    [.71, 0], # Strong / Stark
    [0, .55], # Irritable / Gereizt
    [.66, 0], # Active / Aktiv
    [0, .70], # Afraid / Ǎngstlich
    [.64, 0], # Interessested / Interssiert
    [0, .38], # Hostile / Feindselig
    [.79, 0], # Enthusiastic / Begeistert
    [0, .49], # Ashamed / Beschämt
    [.71 ,0], # Inpsired / Angeregt
    [0, .66], # Jittery / Durcheinander
    [.72, 0], # Alert / Wach
    [0, .64], # Distressed / Bekümmert
    [.44, 0], # Excited / Freudig Erregt
    [0, .60], # Upset / Verärgert
])

l_aist = np.array([
    
])
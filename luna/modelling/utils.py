from .modelling import KalmanFilter
from . import model_settings as MS
import numpy as np
from rest_framework.response import Response
from core.models import StudentUser, Module, StudentSurvey
from .models import FormResults, SurveyResults
from django.utils import timezone
from .serializers import FormResultsSerializer
from core.func import convert_dictionary


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

        # Convert and process each survey
        surveys_matrix = []

        for survey in data:
            converted_values = convert_dictionary(survey)
            surveys_matrix.append(converted_values)

        print(surveys_matrix)

        survey_data = np.array(surveys_matrix)

        print("Student ID, ModuleID", student_id, module_id)
        print("Survey data:", survey_data)

        kalman_filter = KalmanFilter(F=MS.F, H=MS.H, Q=MS.Q, R=MS.R, x0=MS.x0)

        print("Running model...", survey_data)
        print("Survey Data Shape: ", survey_data.shape)
        raw_state, predictions_cov, predictions_obs = kalman_filter.forward(
            survey_data  # eg np.array([[2], [3], [1]])
            # data = np.concat(survey_data, background_data)
        )

        smooth_state, cov_smooth, K = kalman_filter.smooth(
            np.array(raw_state), np.array(predictions_cov)
        )

        raw_state = np.array(raw_state).flatten()
        smooth_state = np.array(smooth_state).flatten()

        for survey, r_state, s_state, r_cov, s_cov in zip(
            surveys, raw_state, smooth_state, predictions_cov, cov_smooth
        ):
            SurveyResults.objects.update_or_create(
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


def process_form(content, student_form):
    try:
        # Convert the content to a NumPy array and ensure the values are numerical
        response_array = np.array(
            [float(value) for key, value in sorted(content.items())]
        )

        print("Processing form for:", student_form.form.name)
        print("Response array:", response_array)

        if student_form.form.name == "PANAS":
            # Perform matrix multiplication
            result = np.dot(response_array, l_panas)
            print("PANAS result:", result)
            # Save the results using the serializer
            data = {"student_form": student_form.pk, "results": result.tolist()}
            print("Data to be saved (PANAS):", data)
            serializer = FormResultsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print("PANAS form saved successfully")
            else:
                print("Serializer errors (PANAS):", serializer.errors)
            return result.tolist()

        elif student_form.form.name == "MOTIVATION":
            # Perform element-wise multiplication and divide by 22
            result = (response_array @ l_motivation) / len(response_array)
            result_list = (
                [result] if isinstance(result, (float, np.float64)) else result.tolist()
            )

            print("Motivation result after averaging:", result_list, type(result_list))

            # Ensure result_list is a list of floats
            if isinstance(result_list[0], (list, np.ndarray)):
                result_list = [float(x) for sublist in result_list for x in sublist]
            else:
                result_list = [float(x) for x in result_list]

            print("Final result list to be saved:", result_list, type(result_list))

            # Save the results using the serializer
            data = {"student_form": student_form.pk, "results": result_list}
            print("Data to be saved (MOTIVATION):", data)
            serializer = FormResultsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print("Motivation form saved successfully")
            else:
                print("Serializer errors (MOTIVATION):", serializer.errors)
            return result_list
        else:
            print("Form type not recognized")
            return None
    except Exception as e:
        print("Error processing form:", str(e))
        return None


# ------------------------------------------------------------------
# Storing the required matricies for the AIST/PANAS etc questionnaires here


# PANAS
# First Entry relates to PA (postive)
# Second Entry relates to NA (negative)

# This is a 20x2 matrix. Use as follows:
# PANAS response: vector of length 20, or matrix of 1x20
# panas_response @ l_aist -> 1x20 @ 20x2 = 1x2 matrix containing PA and NA measurements
l_panas = np.array(
    [
        [0.67, 0],  # Attentive / Aufmerksam
        [0, 0.71],  # Nervous / Nervös
        [0.70, 0],  # Determined / Entschlossen
        [0, 0.70],  # Scared / Erschocken
        [0.58, 0],  # Proud / Stolz
        [0, 0.46],  # Guilty / Schuldig
        [0.71, 0],  # Strong / Stark
        [0, 0.55],  # Irritable / Gereizt
        [0.66, 0],  # Active / Aktiv
        [0, 0.70],  # Afraid / Ǎngstlich
        [0.64, 0],  # Interessested / Interssiert
        [0, 0.38],  # Hostile / Feindselig
        [0.79, 0],  # Enthusiastic / Begeistert
        [0, 0.49],  # Ashamed / Beschämt
        [0.71, 0],  # Inpsired / Angeregt
        [0, 0.66],  # Jittery / Durcheinander
        [0.72, 0],  # Alert / Wach
        [0, 0.64],  # Distressed / Bekümmert
        [0.44, 0],  # Excited / Freudig Erregt
        [0, 0.60],  # Upset / Verärgert
    ]
)

# Motivation
# This we just use the sum score (as in, the sum of the responses).
# In our case though, we should take the mean.
# Some items are negatively coded though, so a mean wouldn't make too much sense.
# Take this matrix/vector, multiply it by the response vector, and then divide by 22 (22=length of array).
# This will give us the positively coded average
l_motivation = np.array(
    [
        1,  # Ich bin gut in Mathematik.
        1,  # Ich beschäftige mich gerne mit Mathematik.
        1,  # Ich finde Mathematik spannend.
        1,  # Mit Mathe-Kenntnissen kann ich andere beeindrucken.
        1,  # Gute Leistungen in Mathe sind mir wichtig.
        1,  # Für meine berufliche Zukunft wird es sich auszahlen, gut in Mathematik zu sein.
        1,  # Es macht mir Spaß, mich mit mathematischen Themen zu beschäftigen.
        -1,  # Ich befürchte, durch den zeitlichen Aufwand im Mathematikstudium wertvolle Freundschaften zu verlieren.
        -1,  # Ich befürchte, dass ich mit dem Stress, den das Mathematikstudium mit sich bringt, nicht umgehen kann
        -1,  # Mathematik hat für mich keine große Bedeutung
        1,  # Es ist mir wichtig, mathematische Inhalte zu meistern.
        -1,  # Für Mathematik fehlt mir die notwendige Begabung
        -1,  # Ich habe den Eindruck, als müsse man für den Abschluss eines Mathematikstudiums mehr Anstrengung investieren, als ich das möchte.
        -1,  # Ich befürchte, dass mir durch das Mathematikstudium Zeit für andere Aktivitäten, die ich gerne verfolgen möchte, verloren geht
        1,  # Gute Leistungen in Mathematik werden mir für Beruf und Karriere viele Vorteile bringen.
        -1,  # Die Beschäftigung mit Mathe kostet mich eine Menge Energie.
        1,  # Mathematik fällt mir leicht.
        1,  # Wenn ich in Mathe viel weiß, komme ich damit bei meinen Kommilitonen gut an.
        -1,  # Mathematik liegt mir nicht besonders.
        1,  # Mathematik macht mir Spaß.
        1,  # Es wäre mir peinlich herauszufinden, wenn meine Leistungen im Mathematikstudium schlechter wären als die meiner Kommilitonen.
        1,  # Mathematik entspricht meinen persönlichen Neigungen.
    ]
)

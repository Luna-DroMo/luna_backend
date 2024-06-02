from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model, extract_features
from rest_framework.response import Response
from core.models import Module, StudentUser, StudentSurvey
from .models import SurveyResults
from django.shortcuts import get_object_or_404
from .serializers import FeatureSerializer, Module_Results_Serializer
from django.db.models import Avg, StdDev
import json
from core.func import generate_survey_matrix
import numpy as np


@api_view(["POST"])
def run(request):
    student_id = request.data.get("student_id")
    module_id = request.data.get("module_id")
    data = run_model(student_id, module_id)

    return Response({"data": data})


@api_view(["GET"])
def get_student_module_modelling_results(request, student_id, module_id):
    module = get_object_or_404(Module, pk=module_id)
    student_surveys = StudentSurvey.objects.filter(student=student_id, module=module)

    if not student_surveys:
        return Response({"error": "No survey data for this student."})

    n_surveys = len(student_surveys)
    survey_matrix = np.zeros((n_surveys, 3))

    for i, survey in enumerate(student_surveys):
        matrix = generate_survey_matrix(survey.content)
        print("SURVEY MATRIX--> ", matrix, type(matrix))
        temp = extract_features(matrix)
        print("EXTRACTED FEATURES--> ", temp, type(temp))
        survey_matrix[i, :] = temp

    survey_matrix = survey_matrix.T  # Each row is a feature, each column is a survey
    print("Survey matrix:", survey_matrix, type(survey_matrix))

    feature_keys = ["understanding", "stress", "content"]
    response = {}

    for i, feature in enumerate(feature_keys):
        feature_data = survey_matrix[i, :]

        response[feature] = feature_data.tolist()

    serializer = FeatureSerializer(data=response)
    serializer.is_valid(raise_exception=True)

    print("RESPONSE-->", response)

    return Response(response)


@api_view(["GET"])
def get_module_modelling_results(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    module_results = (
        SurveyResults.objects.filter(module=module)
        .values("SurveyNumber_T")
        .annotate(
            mean_smoothed_output=Avg("smoothed_output"),
            std_smoothed_output=StdDev(
                "smoothed_output"
            ),  # Calculate standard deviation
        )
        .order_by("SurveyNumber_T")
    )
    serializer = Module_Results_Serializer(module_results, many=True)

    students_high_risk = (
        SurveyResults.objects.filter(module=module, smoothed_output__gt=80)
        .values_list("student_id", flat=True)
        .distinct()
    )
    response_data = {
        "weekly_results": serializer.data,
        "high_risk_students": list(students_high_risk),
    }

    return Response(response_data)

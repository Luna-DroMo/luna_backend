from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model, extract_features
from rest_framework.response import Response
from core.models import Module, StudentUser, StudentSurvey
from .models import SurveyResults
from django.shortcuts import get_object_or_404
from .serializers import (
    FeatureSerializer,
    ModuleResultsSerializer,
    OverviewResultsSerializer,
)
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
    matrices = []

    for i, survey in enumerate(student_surveys):
        print(i, type(survey.content))
        if survey.content:
            print("THERE IS CONTENT")
            matrix = generate_survey_matrix(survey.content)
        else:
            if i == 0:
                print("NO CONTENT, FILL WITH ZEROS")
                matrix = np.zeros((1, 26))  # Use zeros for the first survey
            else:
                print("NO CONTENT, USE PREVIOUS SURVEY")
                matrix = np.copy(
                    matrices[i - 1]
                )  # Use a copy of previous survey's results

        print("matrix-->", matrix)
        matrices.append(np.copy(matrix))
        print("matrices-->", matrices)
        temp = extract_features(matrix)

        survey_matrix[i, :] = temp

    survey_matrix = survey_matrix.T  # Each row is a feature, each column is a survey

    feature_keys = ["understanding", "stress", "content"]
    response = {}

    for i, feature in enumerate(feature_keys):
        feature_data = survey_matrix[i, :]

        response[feature] = feature_data.tolist()

    serializer = FeatureSerializer(data=response)
    serializer.is_valid(raise_exception=True)

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
    serializer = ModuleResultsSerializer(module_results, many=True)

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


@api_view(["GET"])
def get_overview_modelling_results(request):
    results = SurveyResults.objects.aggregate(
        mean_smoothed_output=Avg("smoothed_output"),
        std_smoothed_output=StdDev("smoothed_output"),
    )

    # Format the results as a single dictionary
    formatted_results = {
        "mean_smoothed_output": results["mean_smoothed_output"],
        "std_smoothed_output": results["std_smoothed_output"],
    }

    serializer = OverviewResultsSerializer(formatted_results)
    return Response(serializer.data)

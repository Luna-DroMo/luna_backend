from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model
from rest_framework.response import Response
from core.models import Module, StudentUser
from .models import SurveyResults
from django.shortcuts import get_object_or_404
from .serializers import Student_Module_Results_Serializer, Module_Results_Serializer
from django.db.models import Avg, StdDev
from rest_framework.renderers import JSONRenderer


@api_view(["POST"])
def run(request):
    student_id = request.data.get("student_id")
    module_id = request.data.get("module_id")
    data = run_model(student_id, module_id)

    return Response({"data": data})


@api_view(["GET"])
def get_student_module_modelling_results(request, student_id, module_id):
    module = get_object_or_404(Module, pk=module_id)
    module_results = SurveyResults.objects.filter(module=module, student=student_id)
    serializer = Student_Module_Results_Serializer(module_results, many=True)

    response_data = {
        "weekly_results": serializer.data,
    }

    return Response(response_data)


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

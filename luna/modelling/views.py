from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model
from rest_framework.response import Response
from core.models import StudentSurvey
from .models import Results
from django.shortcuts import get_object_or_404
from .serializers import Student_Module_Results_Serializer


@api_view(["POST"])
def run(request):
    student_id = request.data.get("student_id")
    module_id = request.data.get("module_id")
    data = run_model(student_id, module_id)

    return Response({"data": data})


@api_view(["GET"])
def get_student_module_modelling_results(request, survey_id):
    survey = get_object_or_404(StudentSurvey, pk=survey_id)
    results = Results.objects.filter(student=survey.student, module=survey.module)
    serializer = Student_Module_Results_Serializer(results, many=True)
    return Response(serializer.data)

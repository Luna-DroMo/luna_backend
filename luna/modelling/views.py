from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model
from rest_framework.response import Response
from core.models import Module, StudentUser
from .models import Results
from django.shortcuts import get_object_or_404
from .serializers import Student_Module_Results_Serializer, Module_Results_Serializer


@api_view(["POST"])
def run(request):
    student_id = request.data.get("student_id")
    module_id = request.data.get("module_id")
    data = run_model(student_id, module_id)

    return Response({"data": data})


@api_view(["GET"])
def get_student_module_modelling_results(request, student_id, module_id):
    student = get_object_or_404(StudentUser, pk=student_id)
    module = get_object_or_404(Module, pk=module_id)
    results = Results.objects.filter(student=student, module=module)
    serializer = Student_Module_Results_Serializer(results, many=True)
    return Response(serializer.data)


from django.db.models import FloatField
from django.db.models.aggregates import Aggregate


def get_module_modelling_results(request, module_id):

    module = get_object_or_404(Module, pk=module_id)

    # module_results = (
    #     Results.objects.filter(module=module)
    #     .values("SurveyNumber_T")
    #     .annotate(mean_smoothed_output)
    #     .order_by("SurveyNumber_T")
    # )

    # serializer = Module_Results_Serializer(module_results, many=True)
    # return Response(serializer.data)
    return Response("LOL")

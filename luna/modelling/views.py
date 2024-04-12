from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_model


@api_view(["POST"])
def run(request):
    student_id = request.data.get("student_id")
    survey_id = request.data.get("survey_id")
    data = run_model(student_id, survey_id)

    return Response({"message": "This is a placeholder for the student modelling view"})

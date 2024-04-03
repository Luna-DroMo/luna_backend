from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_student_modelling(request):
    return Response({"message": "This is a placeholder for the student modelling view"})

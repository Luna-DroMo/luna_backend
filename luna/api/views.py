from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import UserSerializer, StudentUserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from core.models import StudentUser, Module, StudentModule, Form, User
from django.shortcuts import get_object_or_404
from .serializers import ModuleSerializer, FormSerializer
import json
from django.http import JsonResponse

# Update the information of a student user


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Succesfully received to endpoint!"})


@api_view(['POST'])
def handle_post(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"status": "success", "data_received": data})


@api_view(["PATCH"])
def update_studentuser_with_id(request, pk):
    try:
        studentuser = StudentUser.objects.get(pk=pk)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        serializer = StudentUserSerializer(
            studentuser,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def save_form(request, student_id):
 
    try:
        studentuser = User.objects.get(pk=student_id)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(studentuser)
    if request.method == "POST":
        form_data = request.data

        # Create a new Form instance with JSON content
        form_instance = Form(user=studentuser, name=form_data['name'], content=form_data['content'])

        # Save the Form instance
        form_instance.save()

        serializer = FormSerializer(instance=form_instance)
        return Response(serializer.data)


@api_view(['GET'])
def get_student_modules(request, student_id):
   # Ensure the student exists
    get_object_or_404(StudentUser, pk=student_id)
    # Retrieve modules related to the student
    student_modules = StudentModule.objects.filter(
        student=student_id).select_related('module')
    print(student_modules)
    modules = [sm.module for sm in student_modules]

    # Serialize the module data
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_studentusers(request):
    if request.method == "GET":
        queryset = StudentUser.objects.all()
        serializer = StudentUserSerializer(queryset, many=True)
        return Response(serializer.data)

    try:
        studentuser = StudentUser.objects.get(email=email)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StudentUserSerializer(studentuser)
        return Response(serializer.data)


# Update the information of a student user
@api_view(["PATCH"])
def update_studentuser_with_email(request, email):
    try:
        studentuser = StudentUser.objects.get(email=email)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        serializer = StudentUserSerializer(
            studentuser,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getUserType(request,id):
    
    user = get_object_or_404(User, id = id)
    # Check to see if user has right password
    #if not user.check_password(request.data["password"]):
    #    return Response(
    #        {"detail": "Not found."},
    #        status=status.HTTP_401_UNAUTHORIZED,
    #    )
    #else:
    return Response(
        user.user_type
    )

@api_view(["POST"])
def createModule(request):

    module_data = request.data

    module_instance = Module(
      module_id = module_data["module_id"],
      name = module_data["name"],
      faculty = module_data["faculty"],
      password = module_data["password"],
      start_date = module_data["start_date"],
      end_date = module_data["end_date"]
      #survey_days = module_data["survey_days"]
    )

    module_instance.save()
    serializer = ModuleSerializer(instance= module_instance)
    return Response(serializer.data)

def save_form(request, student_id):
 
    try:
        studentuser = User.objects.get(pk=student_id)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(studentuser)
    if request.method == "POST":
        form_data = request.data

        # Create a new Form instance with JSON content
        form_instance = Form(user=studentuser, name=form_data['name'], content=form_data['content'])

        # Save the Form instance
        form_instance.save()

        serializer = FormSerializer(instance=form_instance)
        return Response(serializer.data)
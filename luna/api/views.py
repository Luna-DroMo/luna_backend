from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import StudentUser, Module, StudentModule, Form, User, StudentForm
from core.serializers import StudentUserSerializer
from .serializers import ModuleSerializer, FormSerializer, StudentModuleSerializer, StudentFormSerializer, DetailedStudentFormSerializer, DynamicStudentFormSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

import json
from django.http import JsonResponse


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response('+', status=status.HTTP_200_OK)


class ModuleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student_modules = StudentModule.objects.filter(
            student_id=student_id).select_related('module')
        student_module_serializer = StudentModuleSerializer(
            student_modules, many=True)
        return Response(student_module_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            module_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentFormsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, identifier=None):

        student = get_object_or_404(StudentUser, pk=student_id)

        if identifier is None:
            student_forms = StudentForm.objects.filter(student_id=student_id)
            serializer = DynamicStudentFormSerializer(
                student_forms, many=True, context={'exclude_content': True})
            return Response(serializer.data)

        try:
            form_id = int(identifier)
            student_forms = StudentForm.objects.get(
                student_id=student_id, id=form_id)
            serializer = DetailedStudentFormSerializer(student_forms)
        except ValueError:
            if identifier not in dict(Form.FormType.choices):
                return Response({'error': 'Invalid form_type'}, status=status.HTTP_400_BAD_REQUEST)
            student_forms = StudentForm.objects.filter(
                student_id=student_id, form__form_type=identifier)
            serializer = DetailedStudentFormSerializer(
                student_forms, many=True)

        return Response(serializer.data)

    def post(self, request, student_id, identifier=None):
        if identifier is not None:
            return Response({'error': 'Invalid request while submitting the form.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        form_type = data.get('form_type')

        # Fetch the existing StudentForm instance using student_id and form_type
        try:
            student_form = StudentForm.objects.get(
                student_id=student_id,  # Use the correct field name as per your model definition
                form__form_type=form_type  # This assumes `form` is the ForeignKey to the Form model
            )
        except StudentForm.DoesNotExist:
            return Response({"error": "Student form not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize data to update the existing StudentForm instance
        serializer = StudentFormSerializer(
            student_form, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Form updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_form_by_id(self, request, student_id, form_identifier):
        try:
            student_form = StudentForm.objects.select_related('form').get(
                student_id=student_id, form_id=form_identifier
            )
            serializer = DetailedStudentFormSerializer(student_form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentForm.DoesNotExist:
            return Response({'error': 'Student form not found.'}, status=status.HTTP_404_NOT_FOUND)


# Function-based views defined below.
@api_view(['POST'])
def handle_post(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"status": "success", "data_received": data})


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
        form_instance = Form(
            user=studentuser, name=form_data['name'], content=form_data['content'])

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
def get_studentusers(request, email):
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
def getUserType(request, id):

    user = get_object_or_404(User, id=id)
    # Check to see if user has right password
    # if not user.check_password(request.data["password"]):
    #    return Response(
    #        {"detail": "Not found."},
    #        status=status.HTTP_401_UNAUTHORIZED,
    #    )
    # else:
    return Response(
        user.user_type
    )

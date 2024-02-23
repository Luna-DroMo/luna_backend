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
from .serializers import ModuleSerializer, FormSerializer, StudentModuleSerializer, StudentFormSerializer, DetailedStudentFormSerializer
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

    def get(self, request, student_id, form_type=None, form_id=None):
        if not StudentUser.objects.filter(pk=student_id).exists():
            return Response({'error': 'Invalid student_id'}, status=status.HTTP_400_BAD_REQUEST)

        if form_id is not None:
            return self.handle_form_by_id(request, student_id, form_id)

        if form_type and form_type not in dict(Form.FormType.choices):
            return Response({'error': 'Invalid form_type'}, status=status.HTTP_400_BAD_REQUEST)

        if form_type:
            student_forms = StudentForm.objects.filter(
                student_id=student_id, form__form_type=form_type)
        else:
            student_forms = StudentForm.objects.filter(student_id=student_id)

        serializer = StudentFormSerializer(student_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, form_type):
        data = json.loads(request.body)

        for question in data.get("questions", []):
            if question.get("response") in [None, ""]:
                return Response({"error": "Response cannot be null"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_form = StudentForm.objects.get(
                student_id=student_id,
                form__form_type=form_type,
                resolution=StudentForm.ResolutionStatus.NOT_COMPLETED
            )
        except StudentForm.DoesNotExist:
            return Response({"error": "Student form not found or already completed"}, status=status.HTTP_404_NOT_FOUND)

        student_form.content = data.questions
        student_form.resolution = StudentForm.ResolutionStatus.COMPLETED
        student_form.save()

        return Response({"success": "Form updated successfully"}, status=status.HTTP_200_OK)

    def handle_form_by_id(self, request, student_id, form_id):
        try:
            student_form = StudentForm.objects.select_related('form').get(
                student_id=student_id, form_id=form_id
            )
            serializer = DetailedStudentFormSerializer(student_form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentForm.DoesNotExist:
            return Response({'error': 'Student form not found.'}, status=status.HTTP_404_NOT_FOUND)
# Class-based views defined will be refactored according to url discpatcher inside the views.py file.
# class StudentFormsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, student_id, form_type=None, form_id=None):
#         if form_id:
#             return self.handle_form_by_id(request, student_id, form_id)
#         elif form_type:
#             return self.handle_forms_by_type(request, student_id, form_type)
#         else:
#             return self.handle_all_forms(request, student_id)

#     def post(self, request, student_id, form_type=None, form_id=None):
#         if form_type:
#             return self.handle_form_submission(request, student_id, form_type)
#         return Response({"error": "Form type is required for submission."}, status=status.HTTP_400_BAD_REQUEST)

#     def handle_all_forms(self, request, student_id):

#         pass

#     def handle_forms_by_type(self, request, student_id, form_type):

#         pass

#     def handle_form_by_id(self, request, student_id, form_id):
#         pass

#     def handle_form_submission(self, request, student_id, form_type):
#         pass


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

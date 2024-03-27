from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import (
    StudentUser,
    Module,
    StudentModule,
    Form,
    User,
    StudentForm,
    StudentSurvey,
    University,
    Faculty,
)
from .serializers import (
    ModuleSerializer,
    FormSerializer,
    StudentModuleSerializer,
    BackgroundFormSerializer,
    StudentUserSerializer,
    BackgroundStatusSerializer,
    StudentSurveySerializer,
    DisplaySurveySerializer,
    StudentModuleSerializerWithSurveys,
    UniversitySerializer,
    FacultySerializer,
)
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response("+", status=status.HTTP_200_OK)


class ModuleView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get("student_id")
        student_modules = StudentModule.objects.filter(
            student_id=student_id
        ).select_related("module")
        serializer = StudentModuleSerializerWithSurveys(student_modules, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            module_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentFormsView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, student_id, form_id):
        try:
            student = StudentUser.objects.get(pk=student_id)
        except StudentUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            student_form = StudentForm.objects.select_related("form").get(
                student_id=student_id, form_id=form_id
            )
            serializer = BackgroundFormSerializer(student_form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentForm.DoesNotExist:
            return Response(
                {"error": "Student form not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, student_id, form_id):

        try:
            student = StudentUser.objects.get(pk=student_id)
        except StudentUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            student_form = StudentForm.objects.select_related("form").get(
                student_id=student_id, form_id=form_id
            )

            question_ids = {
                question["question_id"]
                for question in student_form.form.content["questions"]
            }

            submitted_responses = request.data
            submitted_question_ids = {
                response["question_id"] for response in submitted_responses
            }

            if question_ids != submitted_question_ids:
                return Response(
                    {"error": "All questions must be answered."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if student_form.content:
                return Response(
                    {"error": "Response already submitted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            student_form.content = submitted_responses
            student_form.resolution = "COMPLETED"
            student_form.submitted_at = timezone.now()
            student_form.save()

            return Response({"message": "Form submitted successfully."})

        except StudentForm.DoesNotExist:
            return Response(
                {"error": "Student form not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    def get(self, request, student_id):
        student = get_object_or_404(StudentUser, pk=student_id)
        serializer = StudentUserSerializer(student)
        return Response(serializer.data)


class SurveyView(APIView):
    def get(self, request, student_id, survey_id):
        student = get_object_or_404(StudentUser, pk=student_id)
        try:
            survey = StudentSurvey.objects.get(
                pk=survey_id, student=student, is_active=True
            )
        except StudentSurvey.DoesNotExist:
            raise Http404("No StudentSurvey matches the given query.")

        serializer = DisplaySurveySerializer(survey)
        return Response(serializer.data)

    def post(self, request, student_id, survey_id):
        student = get_object_or_404(StudentUser, pk=student_id)
        survey = get_object_or_404(StudentSurvey, pk=survey_id)

        if survey.content is not None:
            return Response(
                "Survey already completed.", status=status.HTTP_400_BAD_REQUEST
            )
        if survey.is_active is False:
            return Response("Survey is not active.", status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(survey_status=StudentSurvey.SurveyStatus.COMPLETED)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function-based views defined below.
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_background_status(request, student_id):
    try:
        student = StudentUser.objects.get(pk=student_id)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    student_forms = StudentForm.objects.filter(student_id=student_id).select_related(
        "form"
    )
    total_forms = student_forms.count()

    completed_forms = student_forms.filter(
        resolution=StudentForm.ResolutionStatus.COMPLETED
    )
    not_completed_forms = student_forms.exclude(
        resolution=StudentForm.ResolutionStatus.COMPLETED
    )

    completed_form_types = [form.form.form_type for form in completed_forms]
    not_completed_form_types = [form.form.form_type for form in not_completed_forms]

    percentage = (
        int((len(completed_form_types) / total_forms) * 100) if total_forms > 0 else 0
    )

    personal_info_fields = [
        student.first_name,
        student.last_name,
        student.birth_date,
        student.abitur_note,
        student.main_language,
        student.financial_support,
    ]
    personal_info = all(field is not None for field in personal_info_fields)

    data = {
        "personal_info": "completed" if personal_info else "not_completed",
        "percentage": percentage,
        "completed_forms": completed_form_types,
        "not_completed_forms": not_completed_form_types,
    }

    serializer = BackgroundStatusSerializer(data=data)

    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        form_instance = Form(
            user=studentuser, name=form_data["name"], content=form_data["content"]
        )

        form_instance.save()

        serializer = FormSerializer(instance=form_instance)
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
    return Response(user.user_type)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def enroll_module(request, student_id, module_id):

    try:
        student = StudentUser.objects.get(pk=student_id)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        module = Module.objects.get(pk=module_id)
    except Module.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    password = request.data.get("password")

    if module.password != password:
        return Response(
            {"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST
        )

    if StudentModule.objects.filter(student=student, module=module).exists():
        return Response(
            {"error": "Student is already registered for this module."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    student_module = StudentModule(student=student, module=module)
    student_module.save()

    serializer = StudentModuleSerializer(student_module)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_student_modules(request, student_id):

    student_modules = StudentModule.objects.filter(
        student__user_id=student_id
    ).select_related("module")

    modules = [sm.module for sm in student_modules]

    # serializer = EnrolledModulesSerializer(modules, many=True)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_universities(request):
    universities = University.objects.all()
    serializer = UniversitySerializer(universities, many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(["GET"])
def get_university_faculties(request, university_id):
    university = get_object_or_404(University, pk=university_id)
    faculties = Faculty.objects.filter(university=university)
    serializer = FacultySerializer(faculties, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_lecturer_modules(request, lecturer_id):
    lecturer = get_object_or_404(User, pk=lecturer_id)
    modules = Module.objects.filter(owners_id=lecturer)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_module_details(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    serializer = ModuleSerializer(module)
    return Response(serializer.data)


@api_view(["GET"])
def get_available_modules(request, student_id):

    try:
        student_user = StudentUser.objects.get(user=student_id)
    except StudentUser.DoesNotExist:
        return Response({"error": "Student user not found"}, status=404)

    # Filter modules by student's university and ensure they are within the active date range.
    available_modules = Module.objects.filter(
        faculty__university=student_user.user.university,
    ).exclude(
        studentmodule__student=student_user  # Assuming `studentmodule` is the related name for the relationship.
    )

    serializer = ModuleSerializer([sm.module for sm in available_modules], many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_module(request, format=None):
    serializer = ModuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

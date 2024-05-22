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
from rest_framework.parsers import JSONParser
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
    ActiveSurveySerializer,
    BasicStudentFormSerializer,
)
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError

from modelling.utils import run_model, process_form


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
            student = get_object_or_404(StudentUser, pk=student_id)
        except StudentUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            student_form = StudentForm.objects.select_related("form").get(
                student_id=student_id, form_id=form_id
            )
        except StudentForm.DoesNotExist:
            return Response(
                {"error": "Student form not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if student_form.content:
            return Response(
                {"error": "Response already submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            submitted_responses = request.data

            # Convert the submitted responses into the desired format
            response_dict = {
                response["question_id"]: response["value"]
                for response in submitted_responses
            }

            student_form.content = response_dict
            student_form.resolution = "COMPLETED"
            student_form.submitted_at = timezone.now()
            student_form.save()

            # Process the form based on its type
            try:
                process_form(response_dict, student_form)
            except Exception as e:
                print("Error processing form:", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BasicStudentFormSerializer(student_form)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Unexpected error:", str(e))
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
                pk=survey_id, student=student, status=StudentSurvey.Status.ACTIVE
            )
        except StudentSurvey.DoesNotExist:
            raise Http404("No StudentSurvey matches the given query.")

        serializer = DisplaySurveySerializer(survey)
        return Response(serializer.data)

    parser_classes = [JSONParser]

    def post(self, request, student_id, survey_id):
        student = get_object_or_404(StudentUser, pk=student_id)
        survey = get_object_or_404(StudentSurvey, pk=survey_id)

        if survey.content is not None:
            return Response(
                "Survey already completed.", status=status.HTTP_400_BAD_REQUEST
            )

        content_array = request.data
        if not isinstance(content_array, list):
            return Response(
                {"error": "Invalid data format. Array expected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the survey's content with the array and mark it as completed
        survey.content = content_array
        survey.resolution = StudentSurvey.Resolution.COMPLETED
        survey.status = StudentSurvey.Status.ARCHIVED
        survey.save()

        serializer = StudentSurveySerializer(survey)
        run_model(survey.student_id, survey.module_id)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    completed_form_types = [form.form.name for form in completed_forms]
    not_completed_form_types = [form.form.name for form in not_completed_forms]

    percentage = (
        int((len(completed_form_types) / total_forms) * 100) if total_forms > 0 else 0
    )

    personal_info_fields = [
        student.first_name,
        student.last_name,
    ]
    personal_info = all(field is not None for field in personal_info_fields)

    data = {
        "personal_info": "completed" if personal_info else "not_completed",
        "percentage": percentage,
        "completed_forms": completed_form_types,
        "not_completed_forms": not_completed_form_types,
    }

    print(not_completed_form_types)

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
def enroll_module(request, student_id):

    module_code = request.data["module_code"]
    password = request.data["password"]

    student = get_object_or_404(StudentUser, pk=student_id)
    module = Module.objects.filter(code=module_code).first()
    if not module:
        return Response(
            {"error": "Module not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if module.password != password:
        return Response(
            {"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the student is already enrolled in the module
    if StudentModule.objects.filter(student=student, module=module).exists():
        return Response(
            {"error": "Student is already registered for this module."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    student_module = StudentModule.objects.create(student=student, module=module)
    response_serializer = StudentModuleSerializer(student_module)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


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

    available_modules = Module.objects.filter(
        faculty__university=student_user.user.university,
    )

    serializer = ModuleSerializer([sm for sm in available_modules], many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_module(request, user_id):
    serializer = ModuleSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(owners_id=user_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_university_modules(request, student_id):
    student = get_object_or_404(StudentUser, pk=student_id)
    university = get_object_or_404(University, pk=student.user.university_id)
    modules = Module.objects.filter(university=university)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_active_surveys(request, student_id):
    student = get_object_or_404(StudentUser, pk=student_id)
    surveys = StudentSurvey.objects.filter(
        student=student, status=StudentSurvey.Status.ACTIVE
    )
    serializer = ActiveSurveySerializer(surveys, many=True)
    return Response(serializer.data)

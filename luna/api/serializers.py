from rest_framework import serializers
from core.models import (
    User,
    StudentUser,
    Module,
    Form,
    StudentModule,
    StudentForm,
    StudentSurvey,
    University,
    Faculty,
)
from datetime import datetime, timedelta, date
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["email", "user_type"]


class StudentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentUser
        fields = "__all__"

    # To allow partial updates
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ModuleSerializer(serializers.ModelSerializer):
    survey_end_date = serializers.SerializerMethodField()
    next_survey_date = serializers.SerializerMethodField()
    count_students = serializers.SerializerMethodField()

    class Meta:
        model = Module
        exclude = ["created_at"]

    def get_survey_end_date(self, obj):
        student_id = self.context.get("student_id")
        if student_id:
            print(
                f"Fetching last created survey for student_id: {student_id}, module_id: {obj.id}"
            )
            try:
                # Fetch the latest survey for the student and module
                last_survey = StudentSurvey.objects.filter(
                    student__user_id=student_id, module=obj
                ).latest("created_at")

                # Check the resolution of the survey
                if last_survey.resolution == StudentSurvey.Resolution.COMPLETED:
                    print("Survey is completed, returning None")
                    return None
                else:
                    end_date = last_survey.created_at + timedelta(days=7)
                    print(f"Found last survey with end_date: {end_date}")
                    return end_date
            except StudentSurvey.DoesNotExist:
                print("No survey found")
        return None

    def get_next_survey_date(self, obj):
        student_id = self.context.get("student_id")
        if student_id:
            try:
                # Fetch the latest survey for the student and module
                last_survey = StudentSurvey.objects.filter(
                    student__user_id=student_id, module=obj
                ).latest("created_at")

                # If the last survey is not completed, return its end date
                if last_survey.resolution != StudentSurvey.Resolution.COMPLETED:
                    return last_survey.end_date

                # If the last survey is completed, return created_at + 7 days
                return last_survey.created_at + timedelta(days=7)

            except StudentSurvey.DoesNotExist:
                print("No survey found")
        return None

    def get_count_students(self, obj):
        count_students = StudentModule.objects.filter(module=obj).count()
        return count_students


class LecturerModuleSerializer(serializers.ModelSerializer):
    current_survey_date = serializers.SerializerMethodField()
    next_survey_date = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            "name",
            "code",
            "id",
            "current_survey_date",
            "next_survey_date",
        ]

    def get_current_survey_date(self, obj):
        today = date.today()
        survey_day = int(obj.survey_days)  # Ensure survey_day is an integer
        # Calculate the current survey date, adjusting if today is past the survey day
        if today.weekday() >= survey_day:
            current_survey_date = today - timedelta(days=(today.weekday() - survey_day))
        else:
            current_survey_date = today + timedelta(days=(survey_day - today.weekday()))
        return current_survey_date

    def get_next_survey_date(self, obj):
        today = date.today()
        survey_day = int(obj.survey_days)  # Ensure survey_day is an integer
        # Calculate the next survey date, always in the future
        if today.weekday() >= survey_day:
            next_survey_date = today + timedelta(
                days=(7 - (today.weekday() - survey_day))
            )
        else:
            next_survey_date = today + timedelta(days=(survey_day - today.weekday()))
        return next_survey_date


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"


class StudentModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentModule
        fields = "__all__"


class EnrolledModulesSerializer(serializers.Serializer):
    module_id = serializers.IntegerField(source="id")
    module_name = serializers.CharField(source="name")
    module_start_date = serializers.DateField(source="start_date")

    class Meta:
        model = Module
        fields = ("module_id", "module_name", "module_start_date")


class QuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    response = serializers.CharField()

    def validate_response(self, value):
        if not value.strip():
            raise serializers.ValidationError("Response cannot be null or empty.")
        return value


class StudentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentForm
        fields = "__all__"

    questions = QuestionSerializer(many=True, source="content", write_only=True)

    def validate_content(self, data):
        content = data.get("content", {})

        # Validate form_type if necessary
        form_type = content.get("form_type")
        valid_form_types = Form.objects.values_list("form_type", flat=True).distinct()
        if form_type and form_type not in valid_form_types:
            raise serializers.ValidationError(
                {"content": {"form_type": "Invalid form_type."}}
            )

        # Validate questions and their responses
        questions = content.get("questions", [])
        for question in questions:
            response = question.get("response")
            if response in [None, ""]:
                raise serializers.ValidationError(
                    {"content": {"questions": "Response cannot be null or empty."}}
                )

        return data

    def update(self, instance, validated_data):

        content = validated_data.get("content", {})

        if content:
            instance.content = content
            instance.resolution = StudentForm.ResolutionStatus.COMPLETED
            instance.submitted_at = datetime.now()
            instance.save()

        return instance


class BackgroundFormSerializer(serializers.ModelSerializer):
    form_questions = serializers.SerializerMethodField()
    form_type = serializers.CharField(source="form.form_type")
    resolution = serializers.CharField()
    submitted_at = serializers.DateTimeField()
    response = serializers.CharField(source="content", allow_null=True)

    class Meta:
        model = StudentForm
        fields = [
            "form_questions",
            "form_type",
            "resolution",
            "submitted_at",
            "response",
        ]

    def get_form_questions(self, obj):
        # Accessing form.content directly. You might want to adjust based on your actual content structure.
        return obj.form.content.get("questions", [])


class DynamicStudentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentForm
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        exclude_content = kwargs.pop("context", {}).get("exclude_content", False)
        super(DynamicStudentFormSerializer, self).__init__(*args, **kwargs)
        if exclude_content:
            self.fields.pop("content", None)


class BackgroundStatusSerializer(serializers.Serializer):
    percentage = serializers.IntegerField()
    completed_forms = serializers.ListField(child=serializers.CharField())
    not_completed_forms = serializers.ListField(child=serializers.CharField())
    personal_info = serializers.ChoiceField(
        choices=[("completed", "Completed"), ("not_completed", "Not Completed")]
    )
    form_status = serializers.ChoiceField(
        choices=[("completed", "Completed"), ("not_completed", "Not Completed")]
    )


class StudentSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSurvey
        fields = "__all__"


class ActiveSurveySerializer(serializers.ModelSerializer):
    student = StudentUserSerializer()
    module = ModuleSerializer()

    class Meta:
        model = StudentSurvey
        fields = "__all__"


class DisplaySurveySerializer(serializers.ModelSerializer):
    module_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentSurvey
        fields = [
            "updated_at",
            "module_name",
            "content",
        ]

    def get_module_name(self, obj):
        return obj.module.name if obj.module else None


class StudentModuleSerializerWithSurveys(serializers.Serializer):

    module_name = serializers.CharField(source="module.name", read_only=True)
    module_code = serializers.CharField(source="module.code", read_only=True)
    module_id = serializers.CharField(source="module.id", read_only=True)
    survey_end_date = serializers.SerializerMethodField()
    survey_resolution = serializers.SerializerMethodField()
    survey_created_at = serializers.SerializerMethodField()
    survey_id = serializers.SerializerMethodField()

    class Meta:
        model = StudentModule
        fields = [
            "module_name",
            "module_code",
            "survey_end_date",
            "survey_resolution",
            "survey_created_at",
            "survey_id",
            "module_id",
            "survey_end_date",
        ]

    def get_survey_end_date(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, status=StudentSurvey.Status.ACTIVE
        ).first()
        return survey.end_date if survey else None

    def get_survey_resolution(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, status=StudentSurvey.Status.ACTIVE
        ).first()
        return survey.resolution if survey else None

    def get_survey_created_at(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, status=StudentSurvey.Status.ACTIVE
        ).first()
        return survey.created_at if survey else None

    def get_survey_id(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, status=StudentSurvey.Status.ACTIVE
        ).first()
        return survey.id if survey else None


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name"]


class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = "__all__"


class BasicStudentFormSerializer(serializers.ModelSerializer):
    form_name = serializers.CharField(source="form.name")

    class Meta:
        model = StudentForm
        fields = ["form_name", "resolution", "submitted_at"]


class SurveyInformationSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source="module.name", read_only=True)
    module_code = serializers.CharField(source="module.code", read_only=True)

    class Meta:
        model = StudentSurvey
        fields = ["module_name", "survey_number", "end_date", "module_code"]

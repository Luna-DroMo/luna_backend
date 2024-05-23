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
from datetime import datetime


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


# This one is for module serializer. Since it has built-in support for create update, now no need to add them.
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        exclude = ("password", "created_at")


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
    survey_end_date = serializers.SerializerMethodField()
    survey_is_active = serializers.SerializerMethodField()
    survey_created_at = serializers.SerializerMethodField()
    survey_id = serializers.SerializerMethodField()

    class Meta:
        model = StudentModule
        fields = [
            "module_name",
            "module_code",
            "survey_end_date",
            "survey_is_active",
            "survey_created_at",
            "survey_id",
        ]

    def get_survey_end_date(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, is_active=True
        ).first()
        return survey.end_date if survey else None

    def get_survey_is_active(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, is_active=True
        ).first()
        return survey.is_active if survey else False

    def get_survey_created_at(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, is_active=True
        ).first()
        return survey.created_at if survey else None

    def get_survey_id(self, obj):
        survey = StudentSurvey.objects.filter(
            student=obj.student, module=obj.module, is_active=True
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

    class Meta:
        model = StudentSurvey
        fields = ["module_name", "survey_number", "end_date"]

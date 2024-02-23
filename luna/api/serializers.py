from rest_framework import serializers
from core.models import User, StudentUser, Module, Form, StudentModule, StudentForm


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "__all__"


class StudentUserSerializer(serializers.ModelSerializer):
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
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"


class StudentModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentModule
        fields = "__all__"


class StudentFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentForm
        fields = "__all__"


class DetailedStudentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentForm
        fields = "__all__"

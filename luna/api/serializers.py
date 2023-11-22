from rest_framework import serializers
from core.models import User, StudentUser, Module


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


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['module_id', 'title', 'survey_status', 'next_survey_date']

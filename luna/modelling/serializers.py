from rest_framework import serializers
from .models import Results


class Student_Module_Results_Serializer(serializers.ModelSerializer):
    week = serializers.IntegerField(source="SurveyNumber_T")
    result = serializers.JSONField(source="smoothed_output")

    class Meta:
        model = Results
        fields = ("week", "result")

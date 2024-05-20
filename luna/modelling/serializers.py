from rest_framework import serializers
from .models import Results


class Student_Module_Results_Serializer(serializers.ModelSerializer):
    week = serializers.IntegerField(source="SurveyNumber_T")
    result = serializers.JSONField(source="smoothed_output")

    class Meta:
        model = Results
        fields = ("week", "result")


class Module_Results_Serializer(serializers.Serializer):
    week = serializers.IntegerField(source="SurveyNumber_T")
    mean = serializers.FloatField(source="mean_smoothed_output")
    stdev = serializers.FloatField(source="std_smoothed_output")

from rest_framework import serializers
from .models import SurveyResults, FormResults


class Student_Module_Results_Serializer(serializers.ModelSerializer):
    week = serializers.IntegerField(source="SurveyNumber_T")
    result = serializers.JSONField(source="smoothed_output")

    class Meta:
        model = SurveyResults
        fields = ("week", "result")


class Module_Results_Serializer(serializers.Serializer):
    week = serializers.IntegerField(source="SurveyNumber_T")
    mean = serializers.FloatField(source="mean_smoothed_output")
    stdev = serializers.FloatField(source="std_smoothed_output")


class FormResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResults
        fields = ["student_form", "results"]

    def validate_results(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Results must be a list.")
        if not all(isinstance(i, (float, int)) for i in value):
            raise serializers.ValidationError(
                "All items in results must be float or int."
            )
        return value

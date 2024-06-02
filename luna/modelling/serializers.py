from rest_framework import serializers
from .models import SurveyResults, FormResults


class FeatureSerializer(serializers.Serializer):
    understanding = serializers.ListField(child=serializers.FloatField())
    stress = serializers.ListField(child=serializers.FloatField())
    content = serializers.ListField(child=serializers.FloatField())


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

from django.db import models
from core.models import StudentUser, StudentSurvey


class Results(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentUser, on_delete=models.SET_NULL, null=True)
    survey = models.ForeignKey(StudentSurvey, on_delete=models.CASCADE)
    smoothed_output = models.JSONField(null=True)
    covariance_matrix = models.JSONField(null=True)
    smooth_covariance_matrix = models.JSONField(null=True)
    raw_output = models.JSONField(null=True)
    SurveyNumber_T = models.IntegerField(null=True)
    time_evaluated = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

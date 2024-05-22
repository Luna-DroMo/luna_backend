from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.models import StudentUser, Module, StudentForm


class SurveyResults(models.Model):

    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentUser, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    SurveyNumber_T = models.IntegerField(null=True)
    time_evaluated = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    smoothed_output = models.FloatField(null=True, blank=True)
    covariance_matrix = models.FloatField(null=True, blank=True)
    smooth_covariance_matrix = models.FloatField(null=True, blank=True)
    raw_output = models.FloatField(null=True, blank=True)


class FormResults(models.Model):
    id = models.AutoField(primary_key=True)
    student_form = models.ForeignKey(StudentForm, on_delete=models.SET_NULL, null=True)
    results = ArrayField(models.FloatField(null=True, blank=True))

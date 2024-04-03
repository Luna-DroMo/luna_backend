from django.db import models
from core.models import StudentUser, Module


class Results(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentUser, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    smoothed_output = models.JSONField()
    raw_output = models.JSONField()
    SurveyNumber_T = models.IntegerField()
    time_evaluated = models.DateTimeField(auto_now_add=True)

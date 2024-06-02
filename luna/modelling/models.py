from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.models import StudentUser, Module, StudentForm


class SurveyResults(models.Model):

    class Meta:
        verbose_name = "Modelling Result"
        verbose_name_plural = "Modelling Results"

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
    results = ArrayField(models.FloatField(), null=True, blank=True)

    def student_name(self):
        if self.student_form and self.student_form.student:
            return (
                self.student_form.student.user.first_name
                + " "
                + self.student_form.student.user.last_name
            )
        return None

    def form_name(self):
        if self.student_form and self.student_form.form:
            return self.student_form.form.name
        return None

    student_name.short_description = "Student Name"
    form_name.short_description = "Form Name"

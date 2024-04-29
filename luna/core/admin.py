from django.contrib import admin
from .models import (
    User,
    Module,
    StudentUser,
    StudentModule,
    Form,
    StudentForm,
    Faculty,
    University,
    StudentSurvey,
)


class StudentSurveyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "student",
        "module",
        "survey_number",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("survey_number",)  # make survey_number read-only in the admin


admin.site.register(User)
admin.site.register(Module)
admin.site.register(Form)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(StudentUser)
admin.site.register(StudentModule)
admin.site.register(StudentForm)
admin.site.register(StudentSurvey, StudentSurveyAdmin)

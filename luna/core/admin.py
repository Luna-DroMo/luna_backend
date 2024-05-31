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
        "status",
        "resolution",
    )
    readonly_fields = ("survey_number", "created_at", "updated_at")
    search_fields = (
        "name",
        "student__first_name",
        "student__last_name",
        "module__name",
    )
    list_filter = ("status", "resolution", "created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("name", "student", "module", "survey_number")}),
        ("Dates", {"fields": ("created_at", "start_date", "end_date")}),
        ("Status", {"fields": ("status", "resolution")}),
    )

    actions = ["archive_surveys"]

    def archive_surveys(self, request, queryset):
        queryset.update(status=StudentSurvey.Status.ARCHIVED)

    archive_surveys.short_description = "Archive selected surveys"


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "user_type",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser", "user_type")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "university")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )


class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "university", "owners", "semester", "status")
    search_fields = ("name", "code")
    list_filter = ("university", "semester", "status", "start_date", "end_date")
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "code", "university", "owners", "password")}),
        ("Dates", {"fields": ("start_date", "end_date", "created_at")}),
        ("Schedule", {"fields": ("survey_days",)}),
        ("Status", {"fields": ("semester", "status")}),
    )


class StudentUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "middle_name",
        "last_name",
        "main_language",
        "financial_support",
    )
    search_fields = ("first_name", "last_name", "user__email")
    list_filter = ("main_language", "financial_support")
    ordering = ("user__email",)


class StudentModuleAdmin(admin.ModelAdmin):
    list_display = ("student", "module")
    search_fields = ("student__first_name", "student__last_name", "module__name")
    list_filter = ("module",)
    ordering = ("student__last_name", "module__name")


class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by_user", "created_at")
    search_fields = ("name", "created_by_user__email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


class StudentFormAdmin(admin.ModelAdmin):
    list_display = ("student", "form", "submitted_at", "resolution")
    search_fields = ("student__first_name", "student__last_name", "form__name")
    list_filter = ("resolution", "submitted_at")
    ordering = ("-submitted_at",)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "university", "created_at", "updated_at")
    search_fields = ("name", "university__name")
    list_filter = ("university", "created_at", "updated_at")
    ordering = ("name",)


class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    ordering = ("name",)


admin.site.register(User, UserAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(StudentModule, StudentModuleAdmin)
admin.site.register(StudentForm, StudentFormAdmin)
admin.site.register(StudentSurvey, StudentSurveyAdmin)

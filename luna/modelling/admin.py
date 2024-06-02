from django.contrib import admin
from .models import SurveyResults, FormResults


class SurveyResultsAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "module",
        "SurveyNumber_T",
        "time_evaluated",
        "created_at",
        "smoothed_output",
        "covariance_matrix",
        "smooth_covariance_matrix",
        "raw_output",
    )
    readonly_fields = ("SurveyNumber_T", "time_evaluated", "created_at")
    search_fields = ("student__first_name", "student__last_name", "module__name")
    list_filter = ("module", "time_evaluated", "created_at")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("student", "module", "SurveyNumber_T")}),
        ("Evaluation Details", {"fields": ("time_evaluated", "created_at")}),
        (
            "Results",
            {
                "fields": (
                    "smoothed_output",
                    "covariance_matrix",
                    "smooth_covariance_matrix",
                    "raw_output",
                )
            },
        ),
    )

    actions = ["export_selected_survey_results"]

    def export_selected_survey_results(self, request, queryset):
        # Add custom action logic here
        pass

    export_selected_survey_results.short_description = "Export Selected Survey Results"


class FormResultsAdmin(admin.ModelAdmin):
    list_display = (
        "student_form",
        "student_name",
        "form_name",
        "results",
    )
    search_fields = (
        "student_form__student__first_name",
        "student_form__student__last_name",
        "student_form__form__name",
    )
    list_filter = ("student_form",)
    ordering = ("student_form",)

    fieldsets = (
        (None, {"fields": ("student_form",)}),
        ("Results", {"fields": ("results",)}),
    )


# Register your models here.
admin.site.register(SurveyResults, SurveyResultsAdmin)
admin.site.register(FormResults, FormResultsAdmin)

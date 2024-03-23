from django.db import models
from django.utils import timezone
from core.customFields import DayOfTheWeekField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

"""
Django by default supports login via username and password. To implement the functionality to login via email,
we need to create a custom user.
For more information, google this thing. Also study the difference between AbstractUser and AbstractBaseUser.
"""


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, password, first_name, last_name, password, **extra_fields
        )

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # university_id = models.ForeignKey(
    #     'University', on_delete=models.SET_NULL, null=True)

    class UserType(models.IntegerChoices):
        STUDENT = 1
        LECTURER = 2
        ADMIN = 3

    user_type = models.IntegerField(choices=UserType.choices, default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user_type == User.UserType.STUDENT:
            # Create a StudentUser instance
            student_user, created = StudentUser.objects.get_or_create(
                user=self,
                defaults={
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    # Add other fields as needed
                },
            )


class StudentUser(models.Model):
    class UserLanguages(models.TextChoices):
        EN = "EN", "English"
        DE = "DE", "German"
        OTHER = "OTHER", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    abitur_note = models.IntegerField(null=True)
    main_language = models.CharField(choices=UserLanguages.choices, null=True)
    financial_support = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Automatically populate the email field from the associated User instance
        self.email = self.user.email
        super().save(*args, **kwargs)


class Form(models.Model):

    name = models.CharField(max_length=255)
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    # university = models.ForeignKey(
    #     'University', on_delete=models.CASCADE, null=True)

    class FormType(models.TextChoices):
        EQ = "EQ", "EQ"
        IQ = "IQ", "IQ"
        AIST = "AIST", "AIST"

    form_type = models.CharField(
        max_length=50, choices=FormType.choices, default=FormType.EQ
    )


class StudentForm(models.Model):
    student = models.ForeignKey("StudentUser", on_delete=models.CASCADE)
    form = models.ForeignKey("Form", on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(null=True, default=None)

    class ResolutionStatus(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        NOT_COMPLETED = "NOT_COMPLETED", "Not Completed"

    resolution = models.CharField(
        max_length=20,
        choices=ResolutionStatus.choices,
        default=ResolutionStatus.NOT_COMPLETED,
    )
    content = models.JSONField(null=True, default=None)

    class Meta:
        unique_together = ("student", "form")

    def __str__(self):
        return f"{self.user} - {self.name}"


class Module(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=True)
    faculty = models.ForeignKey(
        "Faculty", on_delete=models.CASCADE, null=True, blank=True
    )
    owners = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to=({"user_type": 2, "user_type": 3}),
    )
    password = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField(null=False, default=timezone.now)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    survey_days = DayOfTheWeekField(null=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class StudentModule(models.Model):

    student = models.ForeignKey("StudentUser", on_delete=models.CASCADE)
    module = models.ForeignKey("Module", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "module")

    def __str__(self):
        return f"{self.student} {self.module}"


class StudentSurvey(models.Model):
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    end_date = models.DateTimeField(null=False, default=timezone.now)
    module = models.ForeignKey("Module", on_delete=models.CASCADE)
    student = models.ForeignKey("StudentUser", on_delete=models.CASCADE)
    content = models.JSONField(null=True, blank=True)

    class SurveyStatus(models.TextChoices):
        NOT_COMPLETED = "NOT_COMPLETED"
        COMPLETED = "COMPLETED"

    survey_status = models.CharField(
        max_length=20,
        choices=SurveyStatus.choices,
        default=SurveyStatus.NOT_COMPLETED,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        help_text="If set to False, the survey will not be visible to the student",
    )

    class Meta:
        unique_together = ("module", "is_active")

    def __str__(self):
        return f"{self.name}"


class University(models.Model):
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return f"{self.module} {self.university}"


class Faculty(models.Model):
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)
    university_id = models.ForeignKey("University", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


# Path: luna/core/models.py

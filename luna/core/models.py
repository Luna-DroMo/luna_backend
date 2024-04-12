from django.db import models
from django.utils import timezone
from core.customFields import DayOfTheWeekField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models import Q


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
    university = models.ForeignKey(
        "University", on_delete=models.SET_NULL, null=True, blank=True
    )

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
    created_by_user = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True
    )  # Custom form logic

    class FormType(models.TextChoices):
        EQ = "EQ", "EQ"
        IQ = "IQ", "IQ"
        AIST = "AIST", "AIST"

    form_type = models.CharField(
        max_length=50, choices=FormType.choices, default=FormType.EQ
    )

    def __str__(self):
        return f"{self.name} - {self.created_by_user}"


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
        return f"{self.student} - {self.form}"


class Module(models.Model):
    name = models.CharField(
        max_length=255,
    )
    code = models.CharField(max_length=255)
    university = models.ForeignKey("University", on_delete=models.CASCADE)
    owners = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=Q(user_type=User.UserType.LECTURER)
        | Q(user_type=User.UserType.ADMIN),
    )
    password = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField(null=False, default=timezone.now)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    survey_days = DayOfTheWeekField(null=True)

    class Semester(models.TextChoices):
        WINTER = "WS", "Winter"
        SUMMER = "SS", "Summer"

    semester = models.CharField(
        max_length=2, choices=Semester.choices, blank=True, null=True, default=None
    )

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    status = models.CharField(
        choices=Status.choices,
        default=Status.INACTIVE,
    )

    def __str__(self):
        return f"{self.name} ({self.id})"


class StudentModule(models.Model):
    student = models.ForeignKey("StudentUser", on_delete=models.CASCADE)
    module = models.ForeignKey("Module", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("module", "student")

    def __str__(self):
        return f"{self.student} {self.module}"


class StudentSurvey(models.Model):

    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    start_date = models.DateTimeField(null=False, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    module = models.ForeignKey("Module", on_delete=models.CASCADE)
    student = models.ForeignKey("StudentUser", on_delete=models.CASCADE)
    content = models.JSONField(null=True, blank=True)

    class Resolution(models.TextChoices):
        NOT_COMPLETED = "NOT_COMPLETED"
        COMPLETED = "COMPLETED"

    resolution = models.CharField(
        max_length=20,
        choices=Resolution.choices,
        default=Resolution.NOT_COMPLETED,
        null=True,
    )

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        LATE = "LATE", "Late"
        ARCHIVED = "ARCHIVED", "Archived"

    status = models.CharField(
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return f"{self.module.name} - {self.student.first_name}"


class University(models.Model):
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.name}"


class Faculty(models.Model):
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, default=timezone.now)
    university = models.ForeignKey("University", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

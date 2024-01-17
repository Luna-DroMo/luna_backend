from django.db import models
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


# Create your User Model here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

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

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # user_id = models.IntegerField(primary_key=True)
    email = models.EmailField(
        max_length=254, db_index=True, unique=True
    )  # Add this field
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    abitur_note = models.IntegerField(null=True)
    main_language = models.CharField(
        choices=UserLanguages.choices, null=True)
    financial_support = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Automatically populate the email field from the associated User instance
        self.email = self.user.email
        super().save(*args, **kwargs)


# This is for form table, we are going to connect this one with Form
class Form(models.Model):
    class FormType(models.TextChoices):
        EQ = 'EQ', 'EQ'
        IQ = 'IQ', 'IQ'

    class ResolutionStatus(models.TextChoices):
        DONE = 'COMPLETED', 'Completed'
        ONGOING = 'NOT_COMPLETED', 'Not Completed'

    name = models.CharField(max_length=255)
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Adjust this if User is in a different file
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    form_type = models.CharField(
        max_length=50,
        choices=FormType.choices,
        default=FormType.EQ
    )
    resolution = models.CharField(
        max_length=20,
        choices=ResolutionStatus.choices,
        default=ResolutionStatus.ONGOING
    )


class Module(models.Model):
    resource_id = models.CharField(max_length=10, null=True, unique=True)
    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # Limit choices to LECTURER users
        limit_choices_to={'user_type': [2, 3]}
    )
    owners = models.ManyToManyField(
        User, limit_choices_to=[2, 3], related_name='owners')
    title = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    next_survey_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.resource_id})"


class StudentModule(models.Model):

    class SurveyStatus(models.TextChoices):
        NOT_STARTED = 'Not Started'
        COMPLETED = 'COMPLETED'

    student = models.ForeignKey('StudentUser', on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    # survey_status = models.CharField(
    #     max_length=20,
    #     choices=SurveyStatus.choices,
    #     default=SurveyStatus.NOT_STARTED,
    #     null=True
    # )

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student} {self.module}"

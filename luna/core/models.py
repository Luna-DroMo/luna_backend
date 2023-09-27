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
    # Abstractbaseuser has password, last_login, is_active by default
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False)
    # this field we inherit from PermissionsMixin.

    class UserType(models.IntegerChoices):
        STUDENT = 1
        LECTURER = 2
        ADMIN = 3
        OTHER = 4  # Keeping this for default behaviour

    user_type = models.IntegerField(choices=UserType.choices, default=4)

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


# RIGHT NOW USER AND STUDENT USER HAVE REDUNDANT FIELDS. I HAVE DONE THIS DELIBERATELY, IN ORDER TO WRITE EFFICIENT CODE AND THEN LATER REMOVE REDUNDANCY ON A NEED BASED SYSTEM.
class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # user_id = models.IntegerField(primary_key=True)
    email = models.EmailField(
        max_length=254, db_index=True, unique=True
    )  # Add this field
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    primary_university_student_id = models.CharField(max_length=20, null=True)
    secondary_university_student_id = models.CharField(
        max_length=20, blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Automatically populate the email field from the associated User instance
        self.email = self.user.email
        super().save(*args, **kwargs)

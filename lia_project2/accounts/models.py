from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
import re


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    security_question = models.CharField(max_length=255, blank=True, null=True)
    security_answer = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        if kwargs.get("using", "default") == "default":
            self.full_clean(exclude=["email"])
        else:
            self.validate_email(self.email)

        if self.is_admin:
            self.is_staff = True
            self.is_superuser = True

        if self.pk is None or not self.password.startswith("pbkdf2_sha256$"):
            if not self.password.startswith("pbkdf2_sha256$"):
                self.validate_password(self.password)
                self.set_password(self.password)

        super().save(*args, **kwargs)

    @staticmethod
    def validate_email(email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email: Please enter a valid email address.")

    @staticmethod
    def validate_password(password):
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise ValidationError("Password must contain both letters and numbers.")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return self.username

    class Meta:
        swappable = "AUTH_USER_MODEL"

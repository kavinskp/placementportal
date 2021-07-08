from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff_account=None):
        if not email:
            raise ValueError('missing email')
        user = self.model(
            email=self.normalize_email(email),
            is_staff_account=is_staff_account
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # for this example, nothing special happens here
        user = self.create_user(
            email,
            password=password,
            is_staff_account=True
        )
        user.is_approved = True
        user.is_active = True
        user.has_filled_data = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        (1, "HOD"),
        (2, "Staff"),
        (3, "Student")
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, null=False, blank=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Department(models.Model):
    name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=20)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth', null=True)
    phone_number = models.CharField(max_length=10)
    avatar = models.ImageField('profile pic (1:1 square)', upload_to='user-profile-pic', null=True, blank=True)


class HOD(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name='hod')
    has_filled_profile = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='staffs')
    has_filled_profile = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_no = models.CharField(unique=True, max_length=7)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    is_hosteler = models.BooleanField(null=False)
    has_filled_profile = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['roll_no']

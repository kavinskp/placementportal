from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff_account=None, activation_key=None, key_expires=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            is_staff_account=is_staff_account,
            activation_key=activation_key,
            key_expires=key_expires
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, activation_key=None, key_expires=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            activation_key=activation_key,
            key_expires=key_expires,
            is_staff_account=True
        )
        user.is_approved = True
        user.is_active = True
        user.is_superuser = True
        user.has_filled_profile = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_staff_account = models.BooleanField(default=False)
    has_filled_profile = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser


class Department(models.Model):
    name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class Staff(models.Model):
    DESIGNATION = (
        (1, "Principal"),
        (2, "HOD"),
        (3, "Faculty"),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    staff_id = models.CharField(unique=True, max_length=10)
    designation = models.IntegerField(choices=DESIGNATION)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Department')
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    avatar = models.ImageField('profile pic (1:1 square)', upload_to='user-profile-pic', null=True, blank=True)

    def get_department(self):
        return Department.objects.get(pk=self.department_id)

    def full_name(self):
        name = self.first_name
        if self.middle_name is not None:
            name += ' ' + self.middle_name
        name += ' ' + self.last_name
        return name

    def get_designation(self):
        return self.get_designation_display()

    def email(self):
        return self.user.email


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_no = models.CharField(unique=True, max_length=7)
    is_hosteler = models.BooleanField(null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Department')
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    avatar = models.ImageField('profile pi1c (1:1 square)', upload_to='user-profile-pic', null=True, blank=True)

    def get_department(self):
        return Department.objects.get(pk=self.department_id)

    def full_name(self):
        name = self.first_name
        if self.middle_name is not None:
            name += ' ' + self.middle_name
        name += ' ' + self.last_name
        return name

    def email(self):
        return self.user.email

    class Meta:
        ordering = ['roll_no']

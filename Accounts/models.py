import enum

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from Curriculum.models import Department, StudentInfo
from Company.models import Company


class UserType(enum.Enum):
    ADMIN = 1
    STAFF = 2
    STUDENT = 3
    INTERVIEWER = 4


class UserTypeValue(enum.Enum):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    STUDENT = 'Student'
    INTERVIEWER = 'Interviewer'


USER_TYPES = (
    (1, 'Admin'),
    (2, 'Staff'),
    (3, 'Student'),
    (4, 'Interviewer')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, activation_key=None,
                    key_expires=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type,
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
            user_type=UserType.ADMIN.value,
            activation_key=activation_key,
            key_expires=key_expires
        )
        user.is_superuser = True
        user.is_verified = True
        user.is_approved = True
        user.save(using=self._db)
        return user


class UserProfile(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    avatar = models.ImageField(upload_to='user-profile-pic', null=True, blank=True)

    def full_name(self):
        name = self.first_name
        if self.middle_name is not None:
            name += ' ' + self.middle_name
        name += ' ' + self.last_name
        return name

    def get_profile_pic(self):
        if self.avatar is not None and self.avatar != "":
            return self.avatar.url
        if self.gender == 'F':
            return "media/images/female.png"
        return "media/images/male.png"

    def __str__(self):
        return self.full_name()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_type = models.SmallIntegerField(choices=USER_TYPES)
    has_filled_profile = models.BooleanField(default=False)
    account_created = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    marked_inactive = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_active(self):
        if not self.marked_inactive and self.is_verified and \
                self.account_created and self.has_filled_profile and self.is_approved:
            return True
        else:
            return False


class StaffAccount(models.Model):
    DESIGNATION = (
        (1, 'Principal'),
        (2, 'HOD'),
        (3, 'Faculty')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    staff_id = models.CharField(unique=True, max_length=10)
    designation = models.SmallIntegerField(choices=DESIGNATION, default=3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Department')

    def full_name(self):
        return self.user.profile.full_name()

    def email(self):
        return self.user.email

    def get_id(self):
        return self.staff_id

    def __str__(self):
        return self.full_name()


class StudentAccount(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    info = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)

    def department(self):
        return self.info.department

    def batch(self):
        return self.info.batch

    def roll_no(self):
        return self.info.roll_no

    def get_id(self):
        return self.roll_no()

    def email(self):
        return self.user.email

    def full_name(self):
        return self.user.profile.full_name()

    def __str__(self):
        return self.full_name()


class InterviewerAccount(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def email(self):
        return self.user.email

    def __str__(self):
        return self.user.profile.full_name()

import enum

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from Curriculum.models import Department, StudentInfo, Batch
from Company.models import CompanyInfo


class UserType(enum.Enum):
    COLLEGE_ADMIN = 1
    STAFF = 2
    STUDENT = 3
    INTERVIEWER = 4


class UserTypeValue(enum.Enum):
    COLLEGE_ADMIN = 'Admin'
    STAFF = 'Staff'
    STUDENT = 'Student'
    INTERVIEWER = 'Interviewer'


class UserGroups(enum.Enum):
    PRINCIPAL = 'Principal'
    HOD = 'HOD'
    FACULTY = 'Faculty'
    FACULTY_ADVISOR = 'FacultyAdvisor'
    STUDENT = 'Student'
    PLACEMENT_OFFICER = 'PO'
    PLACEMENT_REPRESENTATIVE = 'PR'
    RECRUITER = 'recruiter'

    def group_name(self):
        return self.value


class UserPermissions(enum.Enum):
    CAN_APPROVE_STAFF = ('Accounts', 'can_approve_staff', 'Can approve Staff accounts')
    CAN_APPROVE_STUDENT = ('Accounts', 'can_approve_student', 'Can approve Student accounts')
    CAN_APPROVE_INTERVIEWER = ('Accounts', 'can_approve_interviewer', 'Can approve Interviewer accounts')
    CAN_ASSIGN_HOD = ('Curriculum', 'can_assign_hod', 'Can allot HOD for Departments')
    CAN_ASSIGN_FA = ('Curriculum', 'can_assign_fa', 'Can assign Faculty Advisor for Batches')
    CAN_UPDATE_BATCHES = ('Curriculum', 'can_update_batches', 'Can update batch details')
    CAN_ASSIGN_PO = ('Curriculum', 'can_assign_po', 'Can assign Placement officer')
    CAN_ASSIGN_PR = ('Curriculum', 'can_assign_pr', 'Can assign Placement Representative')
    CAN_ASSIGN_POC = ('Curriculum', 'can_assign_poc', 'Can assign Point of Contact for a company')
    CAN_SCHEDULE_INTERVIEW = ('Interview', 'can_schedule_interview', 'Can schedule interview')
    CAN_UPDATE_COMPANY_DETAILS = ('Company', 'can_update_company_details', 'Can update company Details')

    def get_app_label(self):
        return self.value[0]

    def get_code(self):
        return self.value[1]

    def get_description(self):
        return self.value[2]

    def get_permission(self):
        return str(self.get_app_label()) + '.' + str(self.get_code())

    def __str__(self):
        return self.get_permission()


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
        Creates and saves a User with the given email, preferredslot of
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
        Creates and saves a superuser with the given email, preferredslot of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            user_type=UserType.COLLEGE_ADMIN.value,
            activation_key=activation_key,
            key_expires=key_expires
        )
        user.is_superuser = True
        user.is_verified = True
        user.is_approved = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserProfile(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
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

    @property
    def get_profile_pic(self):
        if self.avatar is not None and self.avatar != "":
            return self.avatar.url
        if self.gender == 'F':
            return "/media/images/female.png"
        return "/media/images/male.png"

    def __str__(self):
        return self.full_name()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_type = models.SmallIntegerField(choices=USER_TYPES)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
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

    def full_name(self):
        if self.profile is not None:
            return self.profile.full_name()
        return None

    @property
    def is_active_user(self):
        if not self.marked_inactive and self.is_verified and \
                self.account_created and self.has_filled_profile and self.is_approved:
            return True
        else:
            return False

    @property
    def has_filled_profile(self):
        if self.profile is not None:
            return True
        return False

    @property
    def account_created(self):
        try:
            if self.user_type == UserType.COLLEGE_ADMIN.value and self.staffaccount:
                return True
            if self.user_type == UserType.STAFF.value and self.staffaccount:
                return True
            if self.user_type == UserType.STUDENT.value and self.studentaccount:
                return True
            if self.user_type == UserType.INTERVIEWER.value and self.intervieweraccount:
                return True
        except Exception:
            return False
        return False


@receiver(post_save, sender=CustomUser)
def approve_status_post_save(sender, instance, created, *args, **kwargs):
    current_val = instance.is_active_user
    if current_val:
        if not instance.is_active:
            instance.is_active = True
            instance.save()
    else:
        if instance.is_active:
            instance.is_active = False
            instance.save()


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

    def __str__(self):
        return str(self.user)

    def full_name(self):
        return self.user.full_name()

    def get_id(self):
        return self.staff_id


class FacultyAdvisor(models.Model):
    account = models.OneToOneField(StaffAccount, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)


class StudentAccount(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    info = models.OneToOneField(StudentInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    def full_name(self):
        return self.user.full_name()

    def batch(self):
        return self.info.batch

    def roll_no(self):
        return self.info.roll_no

    @property
    def get_id(self):
        return self.roll_no


class InterviewerAccount(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_info = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    def full_name(self):
        return self.user.full_name()

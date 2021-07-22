from django.db import models
from Curriculum.models import Regulation, Department


class Company(models.Model):
    TYPES = (
        (1, 'Product-based'),
        (2, 'Analytics'),
        (3, 'Service-based'),
        (4, 'Insurance'),
        (5, 'Management-Company'),
        (6, 'Finance'),
        (7, 'Consulting'),
        (8, 'Research & Development'),
        (9, 'Education'),
        (10, 'Others')
    )

    fullName = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    website = models.URLField()
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
    type = models.IntegerField(choices=TYPES)
    description = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class HRContactInfo(models.Model):
    PERSONAL_TITLE = (
        (1, 'Mr.'),
        (2, 'Ms.'),
        (3, 'Mrs.'),
    )
    PREF_CONTACT_TYPE = (
        (1, 'Email'),
        (2, 'Phone'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    personal_title = models.SmallIntegerField(choices=PERSONAL_TITLE)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    preferred_contact = models.SmallIntegerField(choices=PREF_CONTACT_TYPE)
    phoneNumber = models.CharField(blank=True, null=True, max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.full_name()

    def full_name(self):
        name = self.first_name
        if self.middle_name is not None:
            name += ' ' + self.middle_name
        name += ' ' + self.last_name
        return name


class Role(models.Model):
    name = models.CharField(max_length=30),
    location = models.CharField(max_length=30),
    description = models.TextField(null=True)
    minPackage = models.FloatField()
    maxPackage = models.FloatField(null=True)
    additional_info = models.FileField(null=True, upload_to='media_placement/documents/')

    def __str__(self):
        return self.name

    def package(self):
        package = str(self.minPackage)
        package += ' - '
        package += str(self.maxPackage)
        return package


class CompanyJob(models.Model):
    JOB_TYPES = (
        (1, 'Full-Time'),
        (2, 'Part-Time'),
        (3, 'Intern'),
        (4, 'Training')
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=JOB_TYPES)
    vacancy = models.SmallIntegerField(blank=True)
    salary_description = models.TextField(null=True)
    bond_description = models.TextField(null=True)
    description = models.TextField()
    jd_document = models.FileField(null=True, upload_to='media_placement/job/')
    roles = models.ManyToManyField(Role)


class Round(models.Model):
    TYPES = (
        (0, 'Undecided'),
        (1, 'Assessment Test'),
        (2, 'Group Round'),
        (3, 'Panel Round'),
        (4, 'Individual Interview'),
        (5, 'Final Discussion'),
        (6, 'HR Discussion'),
        (7, 'CV Review'),
        (8, 'Other Types'),
    )
    STATUS = (
        (0, 'NotStarted'),
        (1, 'Active'),
        (2, 'Finished'),
        (3, 'Cancelled'),
        (4, 'Postponed'),
        (5, 'ToBeContinued'),
    )
    QUESTION_TYPES = (
        (1, 'Technical'),
        (2, 'Non Technical'),
        (3, 'Mixed'),
    )
    TEST_MODES = (
        (1, 'Online'),
        (2, 'Offline'),
        (3, 'Written')
    )
    CONVERSATION_MODE = (
        (1, 'Personal'),
        (2, 'Telephonic'),
        (3, 'Video Call'),
        (4, 'Online'),
        (5, 'Others')
    )
    question_type = models.SmallIntegerField(choices=QUESTION_TYPES)
    type = models.SmallIntegerField(choices=TYPES)
    mode = models.SmallIntegerField(choices=TEST_MODES),
    status = models.SmallIntegerField(choices=STATUS, default=0),
    conversation_mode = models.SmallIntegerField(choices=CONVERSATION_MODE),
    other_medium = models.CharField(max_length=100, null=True),
    sample_questions = models.FileField(null=True, upload_to='media_placement/round/')
    description = models.TextField()


class Criteria(models.Model):
    batch = models.ManyToManyField(Regulation)
    departments_allowed = models.ManyToManyField(Department)
    min_cgpa = models.FloatField(null=True)
    max_cgpa = models.FloatField(null=True)
    min_gpa = models.FloatField(null=True)
    max_gpa = models.FloatField(null=True)
    history = models.IntegerField(null=True)
    current = models.IntegerField(null=True)
    min_x_percentage = models.FloatField(null=True, default=0)
    max_x_percentage = models.FloatField(null=True, default=100)
    min_xii_percentage = models.FloatField(null=True, default=0)
    max_xii_percentage = models.FloatField(null=True, default=100)
    description = models.TextField()


class CompanyInterview(models.Model):
    job = models.ForeignKey(CompanyJob, on_delete=models.CASCADE)
    Round = models.ManyToManyField(Round)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)

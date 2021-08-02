from django.db import models
from Curriculum.models import Regulation, Batch


class CompanyInfo(models.Model):
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
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
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


class Criteria(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    batch = models.ManyToManyField(Batch)
    min_cgpa = models.FloatField(null=True, blank=True)
    max_cgpa = models.FloatField(null=True, blank=True)
    min_gpa = models.FloatField(null=True, blank=True)
    max_gpa = models.FloatField(null=True, blank=True)
    history = models.IntegerField(null=True, blank=True)
    current = models.IntegerField(null=True, blank=True)
    min_x_percentage = models.FloatField(null=True, blank=True)
    max_x_percentage = models.FloatField(null=True, blank=True)
    min_xii_percentage = models.FloatField(null=True, blank=True)
    max_xii_percentage = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['company', 'name']

    def __str__(self):
        return self.name

    def display(self):
        list = "<table>"
        no_criteria = True
        if self.get_required_cgpa():
            no_criteria = False
            list += "<tr><td>CGPA</td><td>" + str(self.get_required_cgpa()) + "</td></tr>"
        if self.get_required_gpa():
            no_criteria = False
            list += "<tr><td>GPA</td><td>" + str(self.get_required_gpa()) + "</td></tr>"
        if self.get_required_10th_percentage():
            no_criteria = False
            list += "<tr><td>10th %</td><td>" + str(self.get_required_10th_percentage()) + "</td></tr>"
        if self.get_required_12th_percentage():
            list += "<tr><td>12th %</td><td>" + str(self.get_required_12th_percentage()) + "</td></tr>"
        if self.current:
            no_criteria = False
            if self.current == 0:
                list += "<tr><td>No outstanding backlogs</td></tr>"
            else:
                list += "<tr><td>Maximum " + str(self.current) + " outstanding backlogs</td></tr>"
        if self.history:
            no_criteria = False
            if self.history == 0:
                list += "<tr><td>No history of backlogs</td></tr>"
            else:
                list += "<tr><td>Maximum " + str(self.history) + " backlogs in history</td></tr>"
        list += "</table>"
        if no_criteria:
            list = "No Criteria"
        return list

    def get_allowed_batches(self):
        batches = self.batch.all()
        allowed_batches = []
        for batch in batches:
            allowed_batches.append(str(batch))
        return allowed_batches

    def get_allowed_batch_html(self):
        list = self.get_allowed_batches()
        html = "<table>"
        for item in list:
            html += "<tr><td>"+str(item)+"</td></tr>"
        html+="</table>"
        return html

    def get_required_cgpa(self):
        cgpa = None
        if self.min_cgpa is not None:
            if self.max_cgpa is not None:
                cgpa = str(self.min_cgpa) + ' - ' + str(self.max_cgpa)
            else:
                cgpa = '> ' + str(self.min_cgpa)
        elif self.max_cgpa is not None:
            cgpa = '< ' + str(self.max_cgpa)
        return cgpa

    def get_required_gpa(self):
        gpa = None
        if self.min_gpa is not None:
            if self.max_gpa is not None:
                gpa = str(self.min_gpa) + ' - ' + str(self.max_gpa)
            else:
                gpa = '> ' + str(self.min_gpa)
        elif self.max_gpa is not None:
            gpa = '< ' + str(self.max_gpa)
        return gpa

    def get_required_10th_percentage(self):
        x_per = None
        if self.min_x_percentage is not None:
            if self.max_x_percentage is not None:
                x_per = str(self.min_x_percentage) + ' - ' + str(self.max_x_percentage)
            else:
                x_per = '> ' + str(self.min_x_percentage)
        elif self.max_x_percentage is not None:
            x_per = '< ' + str(self.max_x_percentage)
        return x_per

    def get_required_12th_percentage(self):
        xii_per = None
        if self.min_xii_percentage is not None:
            if self.max_xii_percentage is not None:
                xii_per = str(self.min_xii_percentage) + ' - ' + str(self.max_xii_percentage)
            else:
                xii_per = '> ' + str(self.min_xii_percentage)
        elif self.max_xii_percentage is not None:
            xii_per = '< ' + str(self.max_xii_percentage)
        return xii_per


class JobRoles(models.Model):
    JOB_TYPES = (
        (1, 'Full-Time'),
        (2, 'Part-Time'),
        (3, 'Intern'),
        (4, 'Training')
    )
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=30)
    type = models.SmallIntegerField(choices=JOB_TYPES)
    location = models.CharField(max_length=30, blank=True, null=True)
    salary_description = models.TextField(blank=True, null=True)
    bond_description = models.TextField(blank=True, null=True)
    vacancy = models.SmallIntegerField(blank=True, null=True)
    minPackage = models.FloatField()
    maxPackage = models.FloatField(blank=True, null=True)
    documents = models.FileField(blank=True, null=True, upload_to='comapany/job/')

    def __str__(self):
        return self.role_name

    def package(self):
        package = str(self.minPackage)
        if self.maxPackage:
            package += ' - '
            package += str(self.maxPackage)
        return package

    def get_criteria(self):
        criterias = InterviewJobs.objects.filter(role_id=self.pk)
        if criterias.exists():
            return InterviewJobs.objects.get(role_id=self.pk).criteria
        return None

    class Meta:
        unique_together = ('company', 'role_name')


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
    sample_questions = models.FileField(null=True, upload_to='comapany/round/')
    description = models.TextField()


class InterviewJobs(models.Model):
    role = models.OneToOneField(JobRoles, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)


class CompanyInterview(models.Model):
    info = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    job = models.ManyToManyField(InterviewJobs)
    Round = models.ManyToManyField(Round)

from django.db import models

from Curriculum.models import Batch


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

    full_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    website = models.URLField()
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
    type = models.IntegerField(choices=TYPES)
    description = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_company_logo(self):
        if self.logo is not None and self.logo != "":
            return self.logo.url
        return "/media/logo/company_logo.jpg"


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
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        name = self.first_name
        if self.middle_name is not None:
            name += ' ' + self.middle_name
        name += ' ' + self.last_name
        return self.get_personal_title_display() + " " + name


def get_string(min_val, max_val):
    val = None
    if min_val is not None:
        if max_val is not None:
            val = str(min_val) + ' - ' + str(max_val)
        else:
            val = '> ' + str(min_val)
    elif max_val is not None:
        val = '< ' + str(max_val)
    return val


class Criteria(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    batch = models.ManyToManyField(Batch)
    min_cgpa = models.FloatField(null=True, blank=True)
    max_cgpa = models.FloatField(null=True, blank=True)
    history = models.IntegerField(null=True, blank=True)
    current = models.IntegerField(null=True, blank=True)
    min_x_percentage = models.FloatField(null=True, blank=True)
    max_x_percentage = models.FloatField(null=True, blank=True)
    min_x11_percentage = models.FloatField(null=True, blank=True)
    max_x11_percentage = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['company', 'name']

    def __str__(self):
        return self.name

    def display(self):
        criteria_str = "<ul>"
        no_criteria = True
        if self.get_required_cgpa() is not None:
            no_criteria = False
            criteria_str += "<li>CGPA " + self.get_required_cgpa() + "</li>"
        if self.get_required_10th_percentage() is not None:
            no_criteria = False
            criteria_str += "<li>10th % " + str(self.get_required_10th_percentage()) + "</li>"
        if self.get_required_12th_percentage() is not None:
            criteria_str += "<li>12th % " + str(self.get_required_12th_percentage()) + "</li>"
        if self.current is not None:
            no_criteria = False
            if self.current == 0:
                criteria_str += "<li>No outstanding backlogs</li>"
            else:
                criteria_str += "<li>Maximum " + str(self.current) + " outstanding backlogs</li>"
        if self.history is not None:
            no_criteria = False
            if self.history == 0:
                criteria_str += "<li>No history of backlogs</li>"
            else:
                criteria_str += "<li>Maximum " + str(self.history) + " backlogs in history</li>"
        if self.description is not None and self.description != "":
            no_criteria = False
            criteria_str += "<li> Description : " + self.description + "</li>"
        if no_criteria:
            criteria_str += "<li>No Criteria</li>"
        criteria_str += "</ul>"
        return criteria_str

    def get_allowed_batches(self):
        batches = self.batch.all()
        allowed_batches = []
        for batch in batches:
            allowed_batches.append(batch)
        return allowed_batches

    def get_allowed_batch_html(self):
        html = "<ol>"
        for item in self.get_allowed_batches():
            html += "<li>" + str(item) + "</li>"
        html += "</ol>"
        return html

    def get_required_cgpa(self):
        return get_string(self.min_cgpa, self.max_cgpa)

    def get_required_10th_percentage(self):
        return get_string(self.min_x_percentage, self.max_x_percentage)

    def get_required_12th_percentage(self):
        return get_string(self.min_x11_percentage, self.max_x11_percentage)


class CompanyJob(models.Model):
    JOB_TYPES = (
        (1, 'Full-Time'),
        (2, 'Part-Time'),
        (3, 'Intern'),
        (4, 'Training')
    )
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=100)
    type = models.SmallIntegerField(choices=JOB_TYPES)
    location = models.CharField(max_length=30, blank=True, null=True)
    salary_description = models.TextField(blank=True, null=True)
    bond_description = models.TextField(blank=True, null=True)
    vacancy = models.SmallIntegerField(blank=True, null=True)
    minPackage = models.FloatField()
    maxPackage = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE, null=True)
    documents = models.FileField(blank=True, null=True, upload_to='comapany/job/')

    def __str__(self):
        return self.role_name

    def package(self):
        package = str(self.minPackage)
        if self.maxPackage:
            package += ' - '
            package += str(self.maxPackage)
        return package

    class Meta:
        unique_together = ('company', 'role_name')


class RoundInfo(models.Model):
    TYPES = (
        (0, 'Undecided'),
        (1, 'Assessment Test'),
        (2, 'Competitive Coding Round'),
        (3, 'Advanced Coding Round'),
        (4, 'Group Round'),
        (5, 'Panel Round'),
        (6, 'Individual Interview'),
        (7, 'Final Discussion'),
        (8, 'HR Discussion'),
        (9, 'CV Review'),
        (10, 'Other Types'),
    )
    QUESTION_TYPES = (
        (1, 'Technical'),
        (2, 'Non Technical'),
        (3, 'Mixed'),
    )
    TEST_MODES = (
        (1, 'Personal'),
        (2, 'Telephonic'),
        (3, 'Video Call'),
        (4, 'Online'),
        (5, 'Offline (System)'),
        (6, 'Written'),
        (7, 'Group'),
        (8, 'Others')
    )
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    question_type = models.SmallIntegerField(choices=QUESTION_TYPES)
    type = models.SmallIntegerField(choices=TYPES)
    mode = models.SmallIntegerField(choices=TEST_MODES)
    medium = models.CharField(max_length=100, null=True, blank=True, verbose_name='Application / Website Name')
    sample_questions = models.FileField(null=True, blank=True, upload_to='company/round/')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.get_type_display() + ' ( ' + self.get_mode_display() + ' )'

class PreferenceSchedulePeriod(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ['company', 'schedule_date']

    def get_date(self):
        return self.schedule_date.strftime('%d/%m/%Y')

    def get_start_time(self):
        return self.start_time.strftime('%I:%M %p')

    def get_end_time(self):
        return self.end_time.strftime('%I:%M %p')

    def __str__(self):
        return str(self.get_date()) + " - " + str(self.get_start_time()) + " - " + str(self.get_end_time())

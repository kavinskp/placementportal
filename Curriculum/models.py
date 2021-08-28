from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Regulation(models.Model):
    PROGRAMME_CHOICES = (
        ('UG', 'Under Graduate'),
        ('PG', 'Post Graduate'),
        ('Phd', 'Doctorate of Philosophy'),
    )
    start_year = models.SmallIntegerField()
    end_year = models.SmallIntegerField(null=True, blank=True)
    programme_period = models.PositiveSmallIntegerField()
    programme = models.CharField(max_length=3, choices=PROGRAMME_CHOICES)
    current_semester = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        start_year = self.start_year
        end_year = self.get_end_year()
        return str(start_year) + '-' + str(end_year) + " - " + self.programme

    def get_end_year(self):
        start_year = self.start_year
        if self.end_year is None:
            return start_year + self.programme_period
        return self.end_year

    class Meta:
        unique_together = ('programme', 'start_year')


class Batch(models.Model):
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    interview_allowed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.regulation) + ' ' + str(self.department)

    def current_semester(self):
        return self.regulation.current_semester

    class Meta:
        unique_together = ('regulation', 'department')


class StudentInfo(models.Model):
    roll_no = models.CharField(unique=True, max_length=7)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    is_hosteler = models.BooleanField(null=False)
    x_year = models.SmallIntegerField()
    x_percentage = models.FloatField()
    x11_year = models.SmallIntegerField()
    x11_percentage = models.FloatField()
    cgpa = models.FloatField(default=0.0)
    current_backlogs = models.SmallIntegerField(default=0)
    history_of_backlogs = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['roll_no']


class SemesterMarksUpdate(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    cgpa = models.FloatField(default=0.0)
    current_backlogs = models.SmallIntegerField(default=0)
    history_of_backlogs = models.SmallIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

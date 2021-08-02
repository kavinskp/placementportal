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
    end_year = models.SmallIntegerField(null=True)
    programme_period = models.IntegerField()
    programme = models.CharField(max_length=3, choices=PROGRAMME_CHOICES)

    def __str__(self):
        start_year = self.start_year
        end_year = self.get_end_year()
        return str(start_year) + '-' + str(end_year) + " - " + self.programme

    def get_end_year(self):
        start_year = self.start_year
        if self.end_year is None:
            return start_year + self.programme_period
        return self.end_year


class Batch(models.Model):
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    current_semester = models.SmallIntegerField(default=0)
    in_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.regulation) + ' ' + self.department.name

    class Meta:
        unique_together = ('regulation', 'department')


class StudentInfo(models.Model):
    roll_no = models.CharField(unique=True, max_length=7)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    is_hosteler = models.BooleanField(null=False)
    cgpa = models.FloatField(default=0.0)
    current_backlogs = models.SmallIntegerField(default=0)
    history_of_backlog = models.SmallIntegerField(default=0)
    x_year = models.SmallIntegerField()
    x_percentage = models.FloatField()
    xii_year = models.SmallIntegerField()
    xii_percentage = models.FloatField()

    class Meta:
        ordering = ['roll_no']

    @property
    def department(self):
        return self.batch.department

    def get_current_semester(self):
        return self.batch.current_semester


class SemesterMarksUpdate(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    cgpa = models.FloatField(default=0.0)
    current_backlogs = models.SmallIntegerField(default=0)
    history_of_backlog = models.SmallIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

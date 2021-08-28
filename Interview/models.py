from django.db import models

from Accounts.models import StudentAccount, CustomUser, UserPermissions
from Company.models import CompanyJob, CompanyInfo, RoundInfo


class Event(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class CompanySlot(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    co_ordinator = models.ManyToManyField(CustomUser)
    slot = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_scheduled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class CompanySchedule(models.Model):
    company = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    poc = models.ManyToManyField(CustomUser)
    slot = models.ManyToManyField(CompanySlot)


class CompanyInterview(models.Model):
    STATUS = (
        (0, 'Not Scheduled'),
        (1, 'Scheduled'),
        (2, 'Finished'),
        (3, 'Cancelled'),
        (4, 'Postponed'),
        (5, 'Active'),
    )
    company = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    schedule = models.ForeignKey(CompanySchedule, on_delete=models.SET_NULL, null=True)
    marked_for_enroll = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=0)


class StudentInterviewEnroll(models.Model):
    ENROLL_STATUS = (
        (-2, 'Blocked'),
        (-1, 'Yet to choose'),
        (0, 'Not interested'),
        (1, 'Interested'),
        (2, 'Flexi Enrolled'),
    )
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    job = models.ForeignKey(CompanyJob, on_delete=models.CASCADE)
    applied = models.IntegerField(choices=ENROLL_STATUS, default=0)


class StudentInterviewRound(models.Model):
    STATUS = (
        (-1, 'Not Decided'),
        (0, 'Failed'),
        (1, 'Passed'),
        (2, 'Skipped'),
        (3, 'FlexiAllowed'),
    )
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    round = models.ForeignKey(RoundInfo, on_delete=models.CASCADE)
    status = models.IntegerField(default=-1, choices=STATUS)


class PlacedStudent(models.Model):
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=30)
    package = models.FloatField()
    bond = models.IntegerField(default=-1)
    location = models.CharField(max_length=30, blank=True, null=True)

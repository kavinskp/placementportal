import datetime

from django.db import models

from Accounts.models import StudentAccount, CustomUser, UserPermissions
from Company.models import CompanyJob, CompanyInfo, RoundInfo, HRContactInfo
from Curriculum.models import Department
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Event(models.Model):
    name = models.CharField(max_length=100)
    allday = models.BooleanField(default=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    bg_color = models.CharField(max_length=20, default='#64B7E6')
    text_color = models.CharField(max_length=20, default='#000000')
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_start_time(self):
        if self.allday:
            return self.start.strftime('%d-%m-%Y')
        else:
            return self.start.strftime('%d-%m-%Y %I:%M %p')

    def get_end_time(self):
        if self.allday:
            end = self.end - datetime.timedelta(minutes=1)
            return end.strftime('%d-%m-%Y')
        else:
            return self.end.strftime('%d-%m-%Y %I:%M %p')

    def is_interview(self):
        try:
            if self.companyevent:
                return True
        except Exception:
            pass
        return False

    def is_college_event(self):
        try:
            if self.collegeevent:
                return True
        except Exception:
            pass
        return False


class CompanyEvent(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    co_ordinator = models.ManyToManyField(HRContactInfo)
    is_scheduled = models.BooleanField(default=False)
    is_approved = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['is_approved']

    def __str__(self):
        return self.event.name


class CollegeEvent(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    co_ordinator = models.ManyToManyField(StudentAccount)


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


class InterviewRound(models.Model):
    job = models.ForeignKey(CompanyJob, on_delete=models.SET_NULL, null=True)
    info = models.ForeignKey(RoundInfo, on_delete=models.CASCADE)
    round_number = models.SmallIntegerField(default=0)
    schedule = models.ManyToManyField(CompanyEvent, blank=True)
    coordinator = models.ManyToManyField(StudentAccount, blank=True)

    class Meta:
        unique_together = ['job', 'round_number']
        ordering = ['round_number']

    def __str__(self):
        return str(self.job) + " - " + str(self.round_number) + " ) " + str(self.info)

    def get_round_number(self):
        rounds = InterviewRound.objects.filter(job=self.job)
        return self.round_number - rounds.first().round_number + 1


@receiver(pre_save, sender=InterviewRound)
def approve_status_post_save(sender, instance, *args, **kwargs):
    round_number = instance.round_number
    job_rounds = InterviewRound.objects.filter(job=instance.job)
    if round_number == 0:
        if job_rounds.exists():
            last_round = job_rounds.last().round_number
        else:
            last_round = 0
        instance.round_number = last_round + 1
        instance.save()
    elif job_rounds.filter(round_number=round_number).exists():
        last_round = job_rounds.last().round_number
        instance.round_number = last_round + 1
        instance.save()


class StudentInterviewRound(models.Model):
    STATUS = (
        (-1, 'Not Decided'),
        (0, 'Failed'),
        (1, 'Passed'),
        (2, 'Skipped'),
        (3, 'FlexiAllowed'),
    )
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    round = models.ForeignKey(InterviewRound, on_delete=models.CASCADE)
    status = models.IntegerField(default=-1, choices=STATUS)


class PlacedStudent(models.Model):
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=30)
    package = models.FloatField()
    bond = models.IntegerField(default=-1)
    location = models.CharField(max_length=30, blank=True, null=True)

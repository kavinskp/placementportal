from django.db import models

# Create your models here.
from Curriculum.models import Department


class Room(models.Model):
    name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    chair_count = models.SmallIntegerField()
    table_count = models.SmallIntegerField()
    projector = models.SmallIntegerField()
    system_count = models.SmallIntegerField()
    internet_connection = models.SmallIntegerField()
    ups_connection = models.SmallIntegerField()




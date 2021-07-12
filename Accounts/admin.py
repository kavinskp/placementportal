from django.contrib import admin
from Accounts.models import Department, Student, Staff, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Student)

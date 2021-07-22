from django.contrib import admin
from Accounts.models import Department, StudentAccount, StaffAccount, CustomUser,UserProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(StaffAccount)
admin.site.register(StudentAccount)
admin.site.register(UserProfile)

from Accounts.models import CustomUser, UserType

admin_email = 'admin@test.com'
admin_password = 'Admin#1234'

CustomUser.objects.create_superuser(email=admin_email, password=admin_password)

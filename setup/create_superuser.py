from Accounts.models import CustomUser

email = 'admin@test.com'
password = 'Admin#1234'

p_user = CustomUser.objects.create_superuser(email=email, password=password)
print('Admin Created')

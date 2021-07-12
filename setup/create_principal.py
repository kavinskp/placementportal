from Accounts.models import CustomUser, Staff, Department
from django.contrib.auth.models import Group

email = 'principal@test.com'
password = 'Admin#1234'
principal_f_name = 'Mr'
principal_l_name = 'Principal'
principal_dob = '1960-01-01'

user = CustomUser.objects.create_superuser(email=email, password=password)
Staff.objects.create(department=Department.objects.get(name='CSE'),
                     designation=1,
                     user=user,
                     staff_id='101',
                     gender='M',
                     first_name=principal_f_name,
                     last_name=principal_l_name,
                     dob=principal_dob)

group = Group.objects.get(name='Principal')
group.user_set.add(user)

print('Principal Created')
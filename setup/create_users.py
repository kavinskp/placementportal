from Accounts.models import CustomUser, StaffAccount, StudentAccount, Department
from django.contrib.auth.models import Group

CustomUser.objects.all().delete()
StaffAccount.objects.all().delete()
StudentAccount.objects.all().delete()

email = 'principal@test.com'
password = 'Admin#1234'
principal_f_name = 'Mr'
principal_l_name = 'Principal'
principal_dob = '1960-01-01'

p_user = CustomUser.objects.create_superuser(email=email, password=password)
StaffAccount.objects.create(department=Department.objects.get(name='General'),
                            designation=1,
                            user=p_user,
                            staff_id='101',
                            gender='M',
                            first_name=principal_f_name,
                            last_name=principal_l_name,
                            dob=principal_dob)

group = Group.objects.get(name='Principal')
group.user_set.add(p_user)

print('Principal Created')

custom_users_set = (
    ('h1@test.com', 'h12345', True), ('h2@test.com', 'h12345', True),
    ('h3@test.com', 'h12345', True), ('h4@test.com', 'h12345', True),
    ('f1@test.com', 'f12345', True), ('f2@test.com', 'f12345', True),
    ('f3@test.com', 'f12345', True), ('f4@test.com', 'f12345', True),
    ('f5@test.com', 'f12345', True), ('f6@test.com', 'f12345', True),
    ('f7@test.com', 'f12345', True), ('f8@test.com', 'f12345', True),
    ('s1@test.com', 's12345', False), ('s2@test.com', 's12345', True),
    ('s3@test.com', 's12345', False), ('s4@test.com', 's12345', True),
    ('s5@test.com', 's12345', False), ('s6@test.com', 's12345', True),
    ('s7@test.com', 's12345', False), ('s8@test.com', 's12345', True),
    ('s9@test.com', 's12345', False), ('s10@test.com', 's12345', True),
    ('s11@test.com', 's12345', False), ('s12@test.com', 's12345', True),
    ('s13@test.com', 's12345', False), ('s14@test.com', 's12345', True),
    ('s15@test.com', 's12345', False), ('s16@test.com', 's12345', True),
    ('s17@test.com', 's12345', False), ('s18@test.com', 's12345', True),
    ('s19@test.com', 's12345', False), ('s20@test.com', 's12345', True),
)

for c_user in custom_users_set:
    user = CustomUser.objects.create_user(email=c_user[0], password=c_user[1], is_staff_account=c_user[2])
    user.is_verified = True
    user.is_active = True
    user.has_filled_profile = False
    user.save()

hod_users_set = (
    ('h1@test.com', 'M', 'CSE', '1970-01-01', '1001'),
    ('h2@test.com', 'F', 'IT', '1970-02-01', '1002'),
    ('h3@test.com', 'F', 'MECH', '1970-03-01', '1003'),
    ('h4@test.com', 'M', 'CIVIL', '1970-04-01', '1004')
)

for i_hod in hod_users_set:
    user = CustomUser.objects.get(email=i_hod[0])
    StaffAccount.objects.create(user=user,
                                designation=2,
                                department=Department.objects.get(name=i_hod[2]),
                                gender=i_hod[1],
                                dob=i_hod[3],
                                staff_id=i_hod[4],
                                first_name=i_hod[2],
                                last_name='HOD'
                                )
    user.has_filled_profile = True
    user.save()
    group = Group.objects.get(name='HOD')
    group.user_set.add(user)
    print('HOD Created ' + user.email)

faculty_users_set = (
    ('f1@test.com', 'M', 'CSE', '1980-01-01', '10001', 'Kumar', 'R'),
    ('f2@test.com', 'F', 'IT', '1980-02-01', '10002', 'Devi', 'S'),
    ('f3@test.com', 'M', 'MECH', '1980-03-01', '10003', 'Rajesh', 'K'),
    ('f4@test.com', 'F', 'CIVIL', '1980-04-01', '10004', 'Sharmila', 'E'),
    ('f5@test.com', 'F', 'CSE', '1980-01-01', '10005', 'Bavani', 'L'),
    ('f6@test.com', 'M', 'IT', '1980-02-01', '10006', 'Ravi', 'M'),
    ('f7@test.com', 'M', 'MECH', '1980-03-01', '10007', 'Sanoj', 'H'),
    ('f8@test.com', 'F', 'CIVIL', '1980-04-01', '10008', 'Priya', 'S')
)

for i_faculty in faculty_users_set:
    user = CustomUser.objects.get(email=i_faculty[0])
    StaffAccount.objects.create(user=user,
                                designation=3,
                                department=Department.objects.get(name=i_faculty[2]),
                                gender=i_faculty[1],
                                dob=i_faculty[3],
                                staff_id=i_faculty[4],
                                first_name=i_faculty[5],
                                last_name=i_faculty[6]
                                )
    user.has_filled_profile = True
    user.save()
    group = Group.objects.get(name='Faculty')
    group.user_set.add(user)
    print('Staff Created  ' + user.email)

student_users_set = (
    ('s1@test.com', 'M', 'CSE', '1997-01-01', 'Kavin', 'P', True),
    ('s2@test.com', 'M', 'CSE', '1996-02-01', 'Thanu', 'K', True),
    ('s3@test.com', 'M', 'CSE', '1997-03-01', 'Sabarish', 'V', True),
    ('s4@test.com', 'F', 'CSE', '1996-04-01', 'Kalpana', 'K', True),
    ('s5@test.com', 'F', 'CIVIL', '1996-05-01', 'Indhu', 'J', True),
    ('s6@test.com', 'M', 'IT', '1996-06-01', 'Yadhu', 'J', True),
    ('s7@test.com', 'M', 'IT', '1997-07-01', 'Vidhu', 'S', False),
    ('s8@test.com', 'F', 'IT', '1998-08-01', 'Hebi', 'A', True),
    ('s9@test.com', 'F', 'IT', '1998-09-01', 'Kalpana', 'C', True),
    ('s10@test.com', 'F', 'CIVIL', '1997-10-01', 'Renu', 'R', True),
    ('s11@test.com', 'M', 'MECH', '1997-11-01', 'Aravinth', 'S', False),
    ('s12@test.com', 'F', 'CSE', '1997-12-01', 'Kaviya', 'S', True),
    ('s13@test.com', 'M', 'CIVIL', '1997-01-02', 'Suku', 'K', True),
    ('s14@test.com', 'F', 'IT', '1997-04-03', 'Fathana', 'S', True),
    ('s15@test.com', 'F', 'CSE', '1997-01-04', 'Ragavi', 'K', True),
    ('s16@test.com', 'M', 'CSE', '1997-02-05', 'Chandru', 'M', False),
    ('s17@test.com', 'M', 'MECH', '1997-03-06', 'Mani', 'J', True),
    ('s18@test.com', 'F', 'MECH', '1997-04-07', 'Gayathiri', 'S', False),
    ('s19@test.com', 'M', 'CSE', '1997-04-08', 'Sathish', 'SG', True),
    ('s20@test.com', 'M', 'IT', '1998-04-09', 'Gokul', 'M', True),
)

new_roll_start = 1100
dep_roll = {}
roll_count = {}
curr_roll = 0
for i_student in student_users_set:
    if dep_roll.__contains__(i_student[2]):
        curr_roll = dep_roll.get(i_student[2])
    else:
        new_roll_start = new_roll_start + 1
        curr_roll = new_roll_start
        dep_roll.update({i_student[2]: curr_roll})
    i = 0
    if roll_count.__contains__(i_student[2]):
        i = roll_count.get(i_student[2])
    i += 1
    roll = str(i)
    if i < 10:
        roll = '0' + str(i)
    roll_no = str(curr_roll) + roll
    roll_count.update({i_student[2]: i})
    user_obj = CustomUser.objects.get(email=i_student[0])
    StudentAccount.objects.create(user=user_obj,
                                  department=Department.objects.get(name=i_student[2]),
                                  gender=i_student[1],
                                  dob=i_student[3],
                                  roll_no=roll_no,
                                  first_name=i_student[4],
                                  last_name=i_student[5],
                                  is_hosteler=i_student[6]
                                  )
    user_obj.has_filled_profile = True
    user_obj.save()
    print('Student Created ' + user_obj.email)

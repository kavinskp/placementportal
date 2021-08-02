from django.contrib.auth.models import Group
from Curriculum.models import Department, Batch, StudentInfo
from Accounts.models import CustomUser, StaffAccount, StudentAccount, UserProfile, UserType, UserGroups
import random

CustomUser.objects.all().delete()
StaffAccount.objects.all().delete()
StudentAccount.objects.all().delete()

p_email = 'p1@test.com'
p_password = 'p12345'
principal_f_name = 'Mr'
principal_l_name = 'Principal'
principal_dob = '1960-01-01'

p_user = CustomUser.objects.create_user(email=p_email, password=p_password, user_type=UserType.COLLEGE_ADMIN.value)
p_user.is_verified = True
prin_prof = UserProfile.objects.create(gender='M',
                                       first_name=principal_f_name,
                                       last_name=principal_l_name,
                                       dob=principal_dob,
                                       phone_number=9874563210,
                                       avatar='user-profile-pic/groot.jpg'
                                       )
p_user.profile = prin_prof
StaffAccount.objects.create(department=Department.objects.get(name='General'),
                            designation=1,
                            user=p_user,
                            staff_id='1',
                            )
p_user.has_filled_profile = True
p_user.account_created = True
p_user.is_approved = True
p_user.save()
group = Group.objects.get(name=UserGroups.PRINCIPAL.group_name())
group.user_set.add(p_user)

print('Principal Created')

custom_users_set = (
    ('h1@test.com', 'h12345', UserType.STAFF), ('h2@test.com', 'h12345', UserType.STAFF),
    ('h3@test.com', 'h12345', UserType.STAFF), ('h4@test.com', 'h12345', UserType.STAFF),
    ('h5@test.com', 'h12345', UserType.STAFF), ('h6@test.com', 'h12345', UserType.STAFF),
    ('h7@test.com', 'h12345', UserType.STAFF), ('h8@test.com', 'h12345', UserType.STAFF),

    ('f1@test.com', 'f12345', UserType.STAFF), ('f2@test.com', 'f12345', UserType.STAFF),
    ('f3@test.com', 'f12345', UserType.STAFF), ('f4@test.com', 'f12345', UserType.STAFF),
    ('f5@test.com', 'f12345', UserType.STAFF), ('f6@test.com', 'f12345', UserType.STAFF),
    ('f7@test.com', 'f12345', UserType.STAFF), ('f8@test.com', 'f12345', UserType.STAFF),
    ('f9@test.com', 'f12345', UserType.STAFF), ('f10@test.com', 'f12345', UserType.STAFF),
    ('f11@test.com', 'f12345', UserType.STAFF), ('f12@test.com', 'f12345', UserType.STAFF),
    ('f13@test.com', 'f12345', UserType.STAFF), ('f14@test.com', 'f12345', UserType.STAFF),
    ('f15@test.com', 'f12345', UserType.STAFF), ('f16@test.com', 'f12345', UserType.STAFF),

    ('s1@test.com', 's12345', UserType.STUDENT), ('s2@test.com', 's12345', UserType.STUDENT),
    ('s3@test.com', 's12345', UserType.STUDENT), ('s4@test.com', 's12345', UserType.STUDENT),
    ('s5@test.com', 's12345', UserType.STUDENT), ('s6@test.com', 's12345', UserType.STUDENT),
    ('s7@test.com', 's12345', UserType.STUDENT), ('s8@test.com', 's12345', UserType.STUDENT),
    ('s9@test.com', 's12345', UserType.STUDENT), ('s10@test.com', 's12345', UserType.STUDENT),
    ('s11@test.com', 's12345', UserType.STUDENT), ('s12@test.com', 's12345', UserType.STUDENT),
    ('s13@test.com', 's12345', UserType.STUDENT), ('s14@test.com', 's12345', UserType.STUDENT),
    ('s15@test.com', 's12345', UserType.STUDENT), ('s16@test.com', 's12345', UserType.STUDENT),
    ('s17@test.com', 's12345', UserType.STUDENT), ('s18@test.com', 's12345', UserType.STUDENT),
    ('s19@test.com', 's12345', UserType.STUDENT), ('s20@test.com', 's12345', UserType.STUDENT),
    ('s21@test.com', 's12345', UserType.STUDENT), ('s22@test.com', 's12345', UserType.STUDENT),
    ('s23@test.com', 's12345', UserType.STUDENT), ('s24@test.com', 's12345', UserType.STUDENT),
    ('s25@test.com', 's12345', UserType.STUDENT), ('s26@test.com', 's12345', UserType.STUDENT),
    ('s27@test.com', 's12345', UserType.STUDENT), ('s28@test.com', 's12345', UserType.STUDENT),
    ('s29@test.com', 's12345', UserType.STUDENT), ('s30@test.com', 's12345', UserType.STUDENT),
    ('s31@test.com', 's12345', UserType.STUDENT), ('s32@test.com', 's12345', UserType.STUDENT),
    ('s33@test.com', 's12345', UserType.STUDENT), ('s34@test.com', 's12345', UserType.STUDENT),
    ('s35@test.com', 's12345', UserType.STUDENT), ('s36@test.com', 's12345', UserType.STUDENT),
    ('s37@test.com', 's12345', UserType.STUDENT), ('s38@test.com', 's12345', UserType.STUDENT),
    ('s39@test.com', 's12345', UserType.STUDENT), ('s40@test.com', 's12345', UserType.STUDENT),
    ('s41@test.com', 's12345', UserType.STUDENT), ('s42@test.com', 's12345', UserType.STUDENT),
    ('s43@test.com', 's12345', UserType.STUDENT), ('s44@test.com', 's12345', UserType.STUDENT),
    ('s45@test.com', 's12345', UserType.STUDENT), ('s46@test.com', 's12345', UserType.STUDENT),
    ('s47@test.com', 's12345', UserType.STUDENT), ('s48@test.com', 's12345', UserType.STUDENT),
    ('s49@test.com', 's12345', UserType.STUDENT), ('s50@test.com', 's12345', UserType.STUDENT),
    ('s51@test.com', 's12345', UserType.STUDENT), ('s52@test.com', 's12345', UserType.STUDENT),
    ('s53@test.com', 's12345', UserType.STUDENT), ('s54@test.com', 's12345', UserType.STUDENT),
    ('s55@test.com', 's12345', UserType.STUDENT), ('s56@test.com', 's12345', UserType.STUDENT),
    ('s57@test.com', 's12345', UserType.STUDENT), ('s58@test.com', 's12345', UserType.STUDENT),
    ('s59@test.com', 's12345', UserType.STUDENT), ('s60@test.com', 's12345', UserType.STUDENT),

    ('hr1@test.com', 'i12345', UserType.INTERVIEWER), ('hr2@test.com', 'i12345', UserType.INTERVIEWER),
    ('hr3@test.com', 'i12345', UserType.INTERVIEWER), ('hr4@test.com', 'i12345', UserType.INTERVIEWER),
    ('hr5@test.com', 'i12345', UserType.INTERVIEWER), ('hr6@test.com', 'i12345', UserType.INTERVIEWER),

)

for c_user in custom_users_set:
    hod_user = CustomUser.objects.create_user(email=c_user[0], password=c_user[1], user_type=c_user[2].value)
    hod_user.is_verified = True
    hod_user.has_filled_profile = False
    hod_user.save()

hod_users_set = (
    ('h1@test.com', 'M', 'CSE', '1970-01-01', '1001', 'Kumaresan', 'K', 9876598765),
    ('h2@test.com', 'F', 'IT', '1970-02-01', '1002', 'Purusothaman', 'R', 9753186420),
    ('h3@test.com', 'M', 'MECH', '1970-03-01', '1003', 'Ravi', 'S', 9632587410),
    ('h4@test.com', 'M', 'CIVIL', '1970-04-01', '1004', 'Manoj', 'V', 9012345678),
    ('h5@test.com', 'F', 'ECE', '1970-01-01', '1005', 'Sathya', 'D'),
    ('h6@test.com', 'F', 'EEE', '1970-02-01', '1006', 'Gowthami', 'R'),
    ('h7@test.com', 'M', 'EIE', '1970-03-01', '1007', 'Ravi', 'Kumar', 'S', 9632587410),
    ('h8@test.com', 'M', 'PROD', '1970-04-01', '1008', 'Tamil', 'Selvan', 'V', 9012345678),
)

for hod in hod_users_set:
    hod_user = CustomUser.objects.get(email=hod[0])
    ava = 'user-profile-pic/hod_male.png'
    if hod[1] == 'F':
        ava = 'user-profile-pic/hod_female.png'
    midd = None
    if len(hod) == 9:
        midd = hod[6]
    phone = None
    last_name = hod[len(hod) - 1]  # if phone number is not given
    try:
        phone = int(hod[len(hod) - 1])
        last_name = hod[len(hod) - 2]
    except ValueError:
        pass
    hod_prof = UserProfile.objects.create(gender=hod[1],
                                          first_name=hod[5],
                                          last_name=last_name,
                                          dob=hod[3],
                                          middle_name=midd,
                                          phone_number=phone,
                                          avatar=ava
                                          )
    hod_user.profile = hod_prof

    StaffAccount.objects.create(department=Department.objects.get(name=hod[2]),
                                user=hod_user,
                                staff_id=hod[4],
                                )
    hod_user.has_filled_profile = True
    hod_user.account_created = True
    hod_user.save()
    group = Group.objects.get(name=UserGroups.FACULTY.group_name())
    group.user_set.add(hod_user)
    print('HOD Created ' + hod_user.email)

faculty_users_set = (
    ('f1@test.com', 'M', 'CSE', '1980-01-01', '10001', 'Kumar', 'R', 9182736450),
    ('f2@test.com', 'F', 'IT', '1980-02-01', '10002', 'Devi', 'S'),
    ('f3@test.com', 'M', 'MECH', '1980-03-01', '10003', 'Rajesh', 'Kumar', 'K', 8796543021),
    ('f4@test.com', 'F', 'CIVIL', '1980-04-01', '10004', 'Sharmila', 'E'),
    ('f5@test.com', 'F', 'CSE', '1980-01-01', '10005', 'Bavani', 'L'),
    ('f6@test.com', 'M', 'ECE', '1980-02-01', '10006', 'Ravi', 'Bishoni', 'M', 9959792363),
    ('f7@test.com', 'M', 'MECH', '1980-03-01', '10007', 'Sanoj', 'H', 7766885588),
    ('f8@test.com', 'F', 'PROD', '1980-04-01', '10008', 'Priya', 'S', 8866886688),
    ('f9@test.com', 'M', 'ECE', '1980-03-03', '10009', 'Gowtham', 'S', 9696968787),
    ('f10@test.com', 'F', 'CIVIL', '1980-04-03', '10010', 'Ranjini', 'L'),
    ('f11@test.com', 'M', 'CSE', '1980-01-03', '10011', 'Divagar', 'M', 9658958955),
    ('f12@test.com', 'F', 'IT', '1980-02-03', '10012', 'Kousalya', 'Devi', 'L', 9854621730),
    ('f13@test.com', 'M', 'EEE', '1980-03-02', '10013', 'Ramesh', 'Kanna', 'D'),
    ('f14@test.com', 'F', 'EIE', '1980-04-02', '10014', 'Nandhini', 'K', 7485961237),
    ('f15@test.com', 'F', 'CSE', '1980-01-02', '10015', 'Jothika', 'P'),
    ('f16@test.com', 'M', 'IT', '1980-02-02', '10016', 'Raj', 'Kumar', 'M'),
)

for faculty in faculty_users_set:
    f_user = CustomUser.objects.get(email=faculty[0])
    x = random.randint(0, 1)
    ava = None
    if x == 1:
        ava = 'user-profile-pic/staff_male.png'
        if faculty[1] == 'F':
            ava = 'user-profile-pic/staff_female.jpeg'
    phone = None
    last_name = faculty[len(faculty) - 1]  # if phone number is not given
    try:
        phone = int(faculty[len(faculty) - 1])
        last_name = faculty[len(faculty) - 2]
    except ValueError:
        pass
    midd = None
    if len(faculty) > 7:
        if len(faculty) == 9:  # both number & m_name available
            midd = faculty[6]
        elif phone is None:  # only m_name available so len=6
            midd = faculty[6]

    hod_prof = UserProfile.objects.create(gender=faculty[1],
                                          first_name=faculty[5],
                                          last_name=last_name,
                                          dob=faculty[3],
                                          middle_name=midd,
                                          phone_number=phone,
                                          avatar=ava
                                          )
    f_user.profile = hod_prof

    StaffAccount.objects.create(department=Department.objects.get(name=faculty[2]),
                                user=f_user,
                                staff_id=faculty[4],
                                )
    f_user.has_filled_profile = True
    f_user.account_created = True
    f_user.save()
    group = Group.objects.get(name=UserGroups.FACULTY.group_name())
    group.user_set.add(f_user)
    print('Faculty Created ' + f_user.email)

student_users_profile_set = (
    ('s1@test.com', 'M', '1997-01-01', 'Kavin', 'P', 9874561230),
    ('s2@test.com', 'M', '1996-02-01', 'Thanu', 'K'),
    ('s3@test.com', 'M', '1997-03-01', 'Sabarish', 'V', 987651234),
    ('s4@test.com', 'F', '1996-04-01', 'Kalpana', 'K'),
    ('s5@test.com', 'F', '1996-05-01', 'Indhu', 'J'),
    ('s6@test.com', 'M', '1996-06-01', 'Yadhu', 'J', 9874512345),
    ('s7@test.com', 'M', '1997-07-01', 'Vidhu', 'S', 9874561221),
    ('s8@test.com', 'F', '1998-08-01', 'Hebi', 'A',),
    ('s9@test.com', 'F', '1998-09-01', 'Kalpana', 'C'),
    ('s10@test.com', 'F', '1997-10-01', 'Renu', 'R'),
    ('s11@test.com', 'M', '1997-11-01', 'Aravinth', 'Shankar', 'S', 9874461230),
    ('s12@test.com', 'F', '1997-12-01', 'Kaviya', 'S'),
    ('s13@test.com', 'M', '1997-01-02', 'Suku', 'K'),
    ('s14@test.com', 'F', '1997-04-03', 'Fathana', 'Mubin', 'S'),
    ('s15@test.com', 'F', '1997-01-04', 'Ragavi', 'K'),
    ('s16@test.com', 'M', '1997-02-05', 'Chandru', 'M'),
    ('s17@test.com', 'M', '1997-03-06', 'Mani', 'Kandan', 'J'),
    ('s18@test.com', 'F', '1997-04-07', 'Gayathiri', 'S'),
    ('s19@test.com', 'M', '1997-04-08', 'Sathish', 'Kumar', 'SG', 9874561233),
    ('s20@test.com', 'M', '1998-04-09', 'Gokul', 'M'),
    ('s21@test.com', 'M', '1997-01-05', 'Gowsik', 'D'),
    ('s22@test.com', 'M', '1996-02-05', 'Karthick', 'CKV'),
    ('s23@test.com', 'M', '1998-03-05', 'Karthik', 'Raj', 'V'),
    ('s24@test.com', 'F', '1996-04-05', 'Divya', 'Priya', 'S', 9874561221),
    ('s25@test.com', 'F', '1996-05-05', 'Jayanthi', 'K'),
    ('s26@test.com', 'M', '1996-06-09', 'Shashank', 'J'),
    ('s27@test.com', 'M', '1997-07-09', 'Gowtham', 'T'),
    ('s28@test.com', 'F', '1998-08-09', 'Hebi', 'A'),
    ('s29@test.com', 'F', '1998-09-09', 'Kaviya', 'C'),
    ('s30@test.com', 'F', '1997-10-11', 'Kunguma', 'Sneka', 'R', 8447475474),
    ('s31@test.com', 'M', '1997-11-11', 'Aravinthan', 'VM'),
    ('s32@test.com', 'F', '1997-12-11', 'Vishali', 'M'),
    ('s33@test.com', 'M', '1998-01-12', 'Vivek', 'Kumar', 'K'),
    ('s34@test.com', 'F', '1997-04-11', 'Sharmila', 'S'),
    ('s35@test.com', 'F', '1997-01-14', 'Sri', 'Divya', 'K', 8956238956),
    ('s36@test.com', 'M', '1997-02-15', 'Merlin', 'M'),
    ('s37@test.com', 'M', '1997-03-16', 'Mani', 'J'),
    ('s38@test.com', 'F', '1997-04-17', 'Gowthami', 'S', 9595969696),
    ('s39@test.com', 'M', '1997-04-18', 'Risath', 'G', 9874561233),
    ('s40@test.com', 'M', '1998-04-19', 'Raj', 'M'),
    ('s41@test.com', 'M', '1997-01-11', 'Manoj', 'Vignesh', 'P', 9874561231),
    ('s42@test.com', 'M', '1996-02-11', 'Rahul', 'K'),
    ('s43@test.com', 'M', '1997-03-11', 'Siddarth', 'V'),
    ('s44@test.com', 'M', '1996-04-11', 'Gokul', 'K'),
    ('s45@test.com', 'M', '1996-05-21', 'Sasi', 'Anand', 'J'),
    ('s46@test.com', 'F', '1996-06-21', 'Manu', 'Shree', 'J'),
    ('s47@test.com', 'M', '1997-07-21', 'Mani', 'Kandan', 'S'),
    ('s48@test.com', 'F', '1996-08-21', 'Hemalatha', 'A'),
    ('s49@test.com', 'F', '1998-09-01', 'Srinithi', 'C'),
    ('s50@test.com', 'F', '1997-10-01', 'Sowmiya', 'R'),
    ('s51@test.com', 'M', '1997-11-21', 'Jenifer', 'S'),
    ('s52@test.com', 'M', '1997-12-21', 'Saravanan', 'S'),
    ('s53@test.com', 'M', '1998-01-22', 'Naveen', 'K'),
    ('s54@test.com', 'F', '1997-04-03', 'Harini', 'S'),
    ('s55@test.com', 'F', '1997-01-04', 'Aarthi', 'G'),
    ('s56@test.com', 'M', '1996-02-25', 'George', 'M'),
    ('s57@test.com', 'M', '1997-03-26', 'Manoj', 'J'),
    ('s58@test.com', 'M', '1997-04-17', 'Saravanan', 'K'),
    ('s59@test.com', 'M', '1997-04-18', 'Sekar', 'R', 9874561234),
    ('s60@test.com', 'M', '1998-04-19', 'Dharsan', 'M'),
)
for profile in student_users_profile_set:
    s_user = CustomUser.objects.get(email=profile[0])

    male_imgs = ('student1.jpeg', 'student2.jpeg', 'student3.jpg', 'student4.jpg')
    female_imgs = ('student_female.jpg', 'student_female1.png', 'student_female2.jpg', 'student_female3.jpeg')
    x = random.randint(0, 4)
    ava = None
    if x > 0:
        if profile[1] == 'M':
            ava = 'user-profile-pic/' + str(male_imgs[x - 1])
        if profile[1] == 'F':
            ava = 'user-profile-pic/' + str(female_imgs[x - 1])

    phone = None
    last_name = profile[len(profile) - 1]  # if phone number is not given
    try:
        phone = int(profile[len(profile) - 1])
        last_name = profile[len(profile) - 2]
    except ValueError:
        pass
    midd = None
    if len(profile) > 5:
        if len(profile) == 7:  # both number & m_name available
            midd = profile[4]
        elif phone is None:  # only m_name available so len=6
            midd = profile[4]

    prof = UserProfile.objects.create(gender=profile[1],
                                      first_name=profile[3],
                                      last_name=last_name,
                                      dob=profile[2],
                                      middle_name=midd,
                                      phone_number=phone,
                                      avatar=ava
                                      )
    s_user.profile = prof
    s_user.has_filled_profile = True
    s_user.save()
    print('Profile Created ' + s_user.email)

student_info_set = (
    ('s1@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s2@test.com', 'CSE', 2015, 'UG', 2015, 2013, True),
    ('s3@test.com', 'CSE', 2016, 'UG', 2016, 2014, True),
    ('s4@test.com', 'ECE', 2014, 'UG', 2014, 2012, True),
    ('s5@test.com', 'CIVIL', 2014, 'UG', 2014, 2012, True),
    ('s6@test.com', 'IT', 2014, 'UG', 2014, 2012, True),
    ('s7@test.com', 'CSE', 2016, 'PG', 2012, 2010, False),
    ('s8@test.com', 'IT', 2016, 'UG', 2016, 2014, True),
    ('s9@test.com', 'PROD', 2014, 'UG', 2014, 2012, True),
    ('s10@test.com', 'CSE', 2016, 'PG', 2012, 2010, True),
    ('s11@test.com', 'EEE', 2014, 'UG', 2014, 2012, False),
    ('s12@test.com', 'CSE', 2016, 'PG', 2012, 2010, True),
    ('s13@test.com', 'EIE', 2014, 'UG', 2014, 2012, True),
    ('s14@test.com', 'IT', 2017, 'PG', 2013, 2011, True),
    ('s15@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s16@test.com', 'ECE', 2015, 'UG', 2015, 2013, False),
    ('s17@test.com', 'MECH', 2014, 'UG', 2014, 2012, True),
    ('s18@test.com', 'MECH', 2015, 'UG', 2015, 2013, False),
    ('s19@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s20@test.com', 'IT', 2014, 'UG', 2014, 2012, True),
    ('s21@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s22@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s23@test.com', 'CSE', 2017, 'UG', 2017, 2015, True),
    ('s24@test.com', 'ECE', 2014, 'UG', 2014, 2012, True),
    ('s25@test.com', 'CIVIL', 2015, 'UG', 2015, 2013, True),
    ('s26@test.com', 'IT', 2015, 'UG', 2015, 2013, True),
    ('s27@test.com', 'IT', 2014, 'UG', 2014, 2012, False),
    ('s28@test.com', 'IT', 2017, 'UG', 2017, 2015, True),
    ('s29@test.com', 'PROD', 2014, 'UG', 2014, 2012, True),
    ('s30@test.com', 'CIVIL', 2015, 'UG', 2015, 2013, True),
    ('s31@test.com', 'EEE', 2014, 'UG', 2014, 2012, False),
    ('s32@test.com', 'CSE', 2015, 'UG', 2015, 2013, True),
    ('s33@test.com', 'EIE', 2014, 'UG', 2014, 2012, True),
    ('s34@test.com', 'IT', 2016, 'UG', 2016, 2014, True),
    ('s35@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s36@test.com', 'ECE', 2017, 'UG', 2017, 2015, False),
    ('s37@test.com', 'MECH', 2014, 'UG', 2014, 2012, True),
    ('s38@test.com', 'MECH', 2014, 'UG', 2014, 2012, False),
    ('s39@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s40@test.com', 'IT', 2014, 'UG', 2014, 2012, True),
    ('s41@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s42@test.com', 'CSE', 2017, 'Phd', 2011, 2009, True),
    ('s43@test.com', 'IT', 2014, 'UG', 2014, 2012, True),
    ('s44@test.com', 'ECE', 2016, 'PG', 2012, 2010, True),
    ('s45@test.com', 'CIVIL', 2014, 'UG', 2014, 2012, True),
    ('s46@test.com', 'IT', 2017, 'PG', 2013, 2011, True),
    ('s47@test.com', 'IT', 2015, 'UG', 2015, 2013, False),
    ('s48@test.com', 'IT', 2014, 'UG', 2014, 2012, True),
    ('s49@test.com', 'PROD', 2014, 'UG', 2014, 2012, True),
    ('s50@test.com', 'CIVIL', 2014, 'UG', 2014, 2012, True),
    ('s51@test.com', 'EEE', 2014, 'UG', 2014, 2012, False),
    ('s52@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s53@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s54@test.com', 'IT', 2014, 'UG', 2014, 2012, True),
    ('s55@test.com', 'CSE', 2015, 'UG', 2015, 2013, True),
    ('s56@test.com', 'ECE', 2014, 'UG', 2014, 2012, False),
    ('s57@test.com', 'MECH', 2014, 'UG', 2014, 2012, True),
    ('s58@test.com', 'CSE', 2017, 'PG', 2013, 2011, False),
    ('s59@test.com', 'CSE', 2014, 'UG', 2014, 2012, True),
    ('s60@test.com', 'CSE', 2016, 'PG', 2012, 2010, True),
)

roll_count = {}
batch_count = {}
dep_id_start = Department.objects.all()[0].pk

for i_student in student_info_set:
    user_obj = CustomUser.objects.get(email=i_student[0])
    department = Department.objects.get(name=i_student[1])
    batch = Batch.objects.get(regulation__start_year=i_student[2], regulation__programme=i_student[3],
                              department=department)
    curr_roll_pre = None
    if batch_count.__contains__(batch.pk):
        curr_roll_pre = batch_count.get(batch.pk)
    else:
        yr = i_student[2] - 2000
        dep_id = (batch.department_id - dep_id_start + 1)
        if batch.regulation.programme == 'PG':
            dep_id = dep_id + 20
        elif batch.regulation.programme == 'Phd':
            dep_id = dep_id + 30
        new_roll_pre = str(yr).zfill(2) + str(dep_id).zfill(2)  # 14
        batch_count.update({batch.pk: new_roll_pre})
        curr_roll_pre = new_roll_pre
    i = 0
    if roll_count.__contains__(batch.pk):
        i = roll_count.get(batch.pk)
    i = i + 1
    roll_no_str = curr_roll_pre + str(i).zfill(3)
    roll_no = int(roll_no_str)
    roll_count.update({batch.pk: i})
    cgpa = round(random.uniform(7.0, 9.5), 2)
    x_perc = round(random.uniform(90, 100), 2)
    xii_prec = round(random.uniform(85, 100), 2)
    curr_blg = 0
    hist_blg = 0
    x = random.randint(0, 3)
    if x == 2:
        x1 = random.randint(1, 6)
        x2 = random.randint(0, 5)
        x2 = x2 + x1
        curr_blg = x1
        hist_blg = x2

    st_info = StudentInfo.objects.create(
        batch=batch,
        roll_no=roll_no,
        is_hosteler=i_student[6],
        x_year=i_student[4],
        xii_year=i_student[5],
        x_percentage=x_perc,
        xii_percentage=xii_prec,
        cgpa=cgpa,
        current_backlogs=curr_blg,
        history_of_backlog=hist_blg
    )

    StudentAccount.objects.create(user=user_obj, info=st_info)
    user_obj.account_created = True
    user_obj.save()
    group = Group.objects.get(name=UserGroups.STUDENT.group_name())
    group.user_set.add(user_obj)
    print('Student Created ' + user_obj.email)

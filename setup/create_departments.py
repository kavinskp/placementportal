from Accounts.models import Department
Department.objects.all().delete()

dept1 = Department(name='CSE', full_name='COMPUTER SCIENCE AND ENGINEERING')
dept2 = Department(name='IT', full_name='INFORMATION TECHNOLOGY')
dept3 = Department(name='ECE', full_name='ELECTRONICS COMMUNICATION ENGINEERING')
dept4 = Department(name='EEE', full_name='ELECTRICAL AND ELECTRONIC ENGINEERING')
dept5 = Department(name='EIE', full_name='ELECTRONICS AND INSTRUMENTATION ENGINEERING')
dept6 = Department(name='MECH', full_name='MECHANICAL ENGINEERING')
dept7 = Department(name='CIVIL', full_name='CIVIL ENGINEERING')
dept8 = Department(name='PROD', full_name='PRODUCT ENGINEERING')
dept9 = Department(name='IBT', full_name='INDUSTRIAL BIO TECHNOLOGY')
dept1.save()
dept2.save()
dept3.save()
dept4.save()
dept5.save()
dept6.save()
dept7.save()
dept8.save()
dept9.save()

print('department created')
from Curriculum.models import Regulation, Batch, Department

Department.objects.all().delete()

departments_set = (
    ('CSE', 'COMPUTER SCIENCE AND ENGINEERING'),
    ('IT', 'INFORMATION TECHNOLOGY'),
    ('ECE', 'ELECTRONICS COMMUNICATION ENGINEERING'),
    ('EEE', 'ELECTRICAL AND ELECTRONIC ENGINEERING'),
    ('EIE', 'ELECTRONICS AND INSTRUMENTATION ENGINEERING'),
    ('MECH', 'MECHANICAL ENGINEERING'),
    ('CIVIL', 'CIVIL ENGINEERING'),
    ('PROD', 'PRODUCT ENGINEERING'),
    ('IBT', 'INDUSTRIAL BIO TECHNOLOGY'),
    ('General', 'General Department')
)
for dep in departments_set:
    Department.objects.create(name=dep[0],
                              full_name=dep[1])

print('department created')

Regulation.objects.all().delete()

regulation_set = (
    (2014, 2, 'PG'),
    (2015, 2, 'PG'),
    (2014, 4, 'UG'),
    (2015, 4, 'UG'),
    (2016, 4, 'UG'),
    (2017, 4, 'UG'),
)

for reg in regulation_set:
    Regulation.objects.create(start_year=reg[0],
                              programme_period=reg[1],
                              programme=reg[2])

print('Regulations created')

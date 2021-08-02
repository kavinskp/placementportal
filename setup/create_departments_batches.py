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
    (2016, 2, 'PG'),
    (2017, 2, 'PG'),
    (2017, 1, 'Phd'),
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


def create_batch(dep, reg):
    current_yr = reg.start_year - 2018
    if current_yr < 0:
        current_yr = -1 * current_yr
    curr_sem = (current_yr * 2) - 1
    batch = Batch.objects.create(department=dep,
                                 regulation=reg,
                                 current_semester=curr_sem)
    print("Batch Created " + str(dep) + " : " + str(batch))


pg_deps = (
    (2016, ('CSE', 'IT', 'ECE', 'EEE')),
    (2017, ('CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL'))
)

phd_deps = (
    (2017, ('CSE', 'IT')),
)

ug_courses = Regulation.objects.filter(programme='UG')
for ug in ug_courses:
    for dep in Department.objects.all().exclude(name='General'):
        create_batch(dep, ug)

for pg_d in pg_deps:
    pg = Regulation.objects.get(start_year=pg_d[0], programme='PG')
    for name in pg_d[1]:
        dep = Department.objects.get(name=name)
        create_batch(dep, pg)

for ph_d in phd_deps:
    reg = Regulation.objects.get(start_year=ph_d[0], programme='Phd')
    for name in ph_d[1]:
        dep = Department.objects.get(name=name)
        create_batch(dep, reg)

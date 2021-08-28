import enum
from Curriculum.models import Department, Batch
from Company.models import CompanyJob, Criteria, HRContactInfo, CompanyInfo

CompanyInfo.objects.all().delete()
HRContactInfo.objects.all().delete()
Criteria.objects.all().delete()
CompanyJob.objects.all().delete()


class TYPES(enum.Enum):
    ProductBased = 1
    Analytics = 2
    ServiceBased = 3
    Insurance = 4
    ManagementCompany = 5
    Finance = 6
    Consulting = 7
    ResearchDevelopment = 8
    Education = 9
    Others = 10


Company_obj_list = (
    ('ZOHO', 'Zoho Corporation Private Private', 'www.zoho.com', TYPES.ProductBased, 'logo/zoho.png'),
    ('Infosys', 'Infosys Limited', 'www.infosys.com', TYPES.ServiceBased, 'logo/infosys.png'),
    ('Accolite', 'Accolite Corporation', 'www.accolite.corp', TYPES.Analytics),
    ('Sirius', 'Sirius Software Solutions', 'www.sirius.com', TYPES.Finance),
    ('Amazon', 'Amazon Web Services', 'www.amazon.jobs', TYPES.ProductBased, 'logo/amazon.jpeg'),
    ('Accenture', 'Accenture corporation Private Private', 'www.accenture.com', TYPES.ResearchDevelopment)
)

description_dict = {
    'Infosys': 'Infosys Limited is an Indian multinational information technology company that provides business consulting, information technology and outsourcing services. The company was founded in Pune and is headquartered in Bangalore',
    'ZOHO': 'Zoho Corporation is an Indian multinational technology company that makes web-based business tools. It is best known for online office suite named Zoho',
}

for entry in Company_obj_list:
    logo = None
    if len(entry) > 4:
        logo = entry[4]
    CompanyInfo.objects.get_or_create(
        name=entry[0],
        full_name=entry[1],
        website=entry[2],
        type=entry[3].value,
        logo=logo,
        description=description_dict.get(entry[0])
    )
    print('Company info - ' + entry[0] + ' created')

hr_set = (
    ('ZOHO', 'jagan@zoho.com', 'Manager', 'Mr', 'Jagan', 'R', 9874561230),
    ('ZOHO', 'abilash@zoho.com', 'Mentor', 'Mr', 'Abilash', 'R'),
    ('ZOHO', 'krishna@zoho.com', 'MLS', 'Mr', 'Krishna', 'Kumar', 'R'),
    ('Infosys', 'kannan@infosys.com', 'HR', 'Mr', 'Kannan', 'K'),
    ('Accolite', 'dhamothiran@accolite.com', 'Manager', 'Mr', 'Dhamothiran', 'V', 987651234),
    ('Sirius', 'cyntia@sirius.com', 'Mentor', 'Ms', 'Cynthia', 'K'),
    ('Amazon', 'jey@amazon.com', 'Manager', 'Mr', 'Jey', 'D', 9874561230),
    ('Amazon', 'harish@amazon.com', 'Senior Engineer', 'Mr', 'Harish', 'Kalyan', 'C'),
    ('Accenture', 'ganesh@accenture.com', 'Lead Manager', 'Mr', 'Ganesh', 'D'),
)

for hr in hr_set:
    phone = None
    last_name = hr[len(hr) - 1]  # if phone number is not given
    try:
        phone = hr[len(hr) - 1]
        last_name = hr[len(hr) - 2]
    except ValueError:
        pass
    midd = None
    if len(hr) > 6:
        if len(hr) == 8:  # both number & m_name available
            midd = hr[5]
        elif phone is None:  # only m_name available so len=6
            midd = hr[5]
    preffered_contact = 1
    if phone is not None:
        preffered_contact = 2

    personal_title = 1
    if hr[3] == 'Ms':
        personal_title = 2
    elif hr[3] == 'Mrs':
        personal_title = 3
    HRContactInfo.objects.create(
        company=CompanyInfo.objects.get(name=hr[0]),
        email=hr[1],
        phoneNumber=phone,
        designation=hr[2],
        personal_title=personal_title,
        first_name=hr[4],
        last_name=last_name,
        middle_name=midd,
        preferred_contact=preffered_contact
    )
    print('HR - ' + hr[1] + ' created')

criteria_set = (
    ('ZOHO', 'No Criteria', []),
    ('Infosys', 'Min 60% CGPA', [], 6.0, None, 0, None),
    ('Infosys', 'Min 70% & No history', [], 8.0, None, 0, 0, 80, None, 80, None),
    ('Accolite', 'Circuit - Min. 8 CGPA', ['CSE', 'IT', 'ECE', 'EEE', 'EIE'], 8.0),
    ('Sirius', 'Min 8 CGPA & No history', [], 8.0, None, 0, 0),
    ('Amazon', 'Min 8.5 CGPA & No history', ['CSE', 'IT'], 8.0, None, 0, 0),
    ('Amazon', 'Min 7 CGPA & No backlogs', [], 7.0, None, 0, None),
    ('Accenture', 'Min. 7.5 CGPA', ['CSE', 'IT', 'ECE', 'EEE', 'EIE', 'MECH', 'CIVIL'], 7.5),
)

criteria_description_dict = {
    'Accenture': 'Python Language basic knowledge needed',
    'Sirius': 'Should have good communication skills'
}

for criteria in criteria_set:
    min_cgpa = criteria[3] if len(criteria) > 3 else None
    max_cgpa = criteria[4] if len(criteria) > 4 else None
    current = criteria[5] if len(criteria) > 5 else None
    history = criteria[6] if len(criteria) > 6 else None
    min_10th = criteria[7] if len(criteria) > 7 else None
    max_10th = criteria[8] if len(criteria) > 8 else None
    min_12th = criteria[9] if len(criteria) > 9 else None
    max_12th = criteria[10] if len(criteria) > 10 else None

    criteria_obj = Criteria.objects.create(
        company=CompanyInfo.objects.get(name=criteria[0]),
        name=criteria[1],
        min_cgpa=min_cgpa,
        max_cgpa=max_cgpa,
        current=current,
        history=history,
        min_x_percentage=min_10th,
        max_x_percentage=max_10th,
        min_x11_percentage=min_12th,
        max_x11_percentage=max_12th,
        description=criteria_description_dict.get(criteria[0])
    )
    allowed_batches = Batch.objects.filter(interview_allowed=True)
    if len(criteria[2]) > 0:
        allowed_batches = Batch.objects.filter(interview_allowed=True, department__name__in=criteria[2])
    for batch in allowed_batches:
        criteria_obj.batch.add(batch)

    print('Criteria for ' + criteria[0] + ' created')

Job_types = {
    'Full-Time': 1,
    'Part-Time': 2,
    'Intern': 3,
    'Training': 4
}

job_set = (
    ('ZOHO', 'Member Technical Staff', 4.6, 6.6, 'No Criteria', 'Full-Time', 'Chennai'),
    ('ZOHO', 'Member Technical Staff - QA', 4.6, 6.6, 'No Criteria', 'Full-Time', 'Chennai'),
    ('Infosys', 'Quality Assuarance Tester', 2.6, None, 'Min 60% CGPA', 'Intern', 'Bengalure'),
    ('Infosys', 'Software Designer', 3.5, None, 'Min 70% & No history', 'Full-Time', 'Chennai', 25),
    ('Accolite', 'Software Engineer', 10, 12, 'Circuit - Min. 8 CGPA', 'Intern', 'Chennai', 10),
    ('Sirius', 'Web Developer', 6, None, 'Min 8 CGPA & No history', 'Part-Time', 'Chennai', 5),
    ('Amazon', 'Software Engineer - I', 24, None, 'Min 8.5 CGPA & No history', 'Intern', 'Hyderabad', 5),
    ('Amazon', 'Quality Assuarance Tester', 18, None, 'Min 7 CGPA & No backlogs', 'Intern', 'Hyderabad'),
    ('Accenture', 'Python Developer', 8, None, 'Min. 7.5 CGPA', 'Full-Time', 'Bengalure,Chennai', 10),
)
bond_description = {
    'Accenture': '2 Years'
}
salay_description = {
    'Amazon': 'Salary is 12LPA during intern period(3 months).'
}
for job in job_set:
    company_obj = CompanyInfo.objects.get(name=job[0])
    CompanyJob.objects.create(
        company=company_obj,
        role_name=job[1],
        minPackage=job[2],
        maxPackage=job[3],
        criteria=Criteria.objects.get(company=company_obj, name=job[4]),
        type=Job_types[job[5]],
        location=job[6],
        vacancy=job[7] if len(job) > 7 else None,
        salary_description=salay_description.get(job[0]),
        bond_description=bond_description.get(job[0])
    )
    print('Job ' + company_obj.name + ' - ' + job[1] + ' created')

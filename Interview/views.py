from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from Curriculum.models import StudentInfo
from Company.models import CompanyJob, CompanyInfo
from Accounts.models import StudentAccount, UserPermissions, UserGroups
from Interview.models import StudentInterviewEnroll, CompanyInterview


def is_po(user):
    if user.groups.filter(name=UserGroups.PLACEMENT_OFFICER.group_name()).exists():
        return True
    return False


def is_pr(user):
    if user.groups.filter(name=UserGroups.PLACEMENT_REPRESENTATIVE.group_name()).exists():
        return True
    return False


def get_company_list(user):
    company_list = None
    if is_po(user):
        company_list = CompanyInfo.objects.filter().distinct()
    elif is_pr(user):
        student_obj = StudentAccount.objects.get(user=user)
        company_list = CompanyInfo.objects.filter(companyjob__criteria__batch=student_obj.info.batch).distinct()
    return company_list


# Create your views here.
@permission_required(UserPermissions.CAN_APPROVE_INTERVIEWER.get_permission())
def manage_companies(request):
    company_list = get_company_list(request.user).distinct()
    return render(request, 'manage_companies.html', {
        'company_list': company_list
    })


@permission_required(UserPermissions.CAN_APPROVE_INTERVIEWER.get_permission())
def view_company_details(request, company_id):
    compan_info = CompanyInfo.objects.get(pk=company_id)
    return render(request, 'view_company_info.html', {
        'company': compan_info
    })


def view_student_list(request, company_id):
    company_obj = CompanyInfo.objects.get(pk=company_id)
    jobs = []
    for job in company_obj.companyjob_set.all():
        job_dict = {}
        job_dict.update({'name': job.role_name})
        student_data_filled = False
        try:
            company_interview = CompanyInterview.objects.get(company_id=company_id)
            if company_interview.marked_for_enroll:
                interested_students = StudentInterviewEnroll.objects.filter(job=job, applied__gt=0)
                not_interested_students = StudentInterviewEnroll.objects.filter(job=job, applied__lt=0)
                undecided_students = StudentInterviewEnroll.objects.filter(job=job, applied=0)
                job_dict.update({'interested_students': interested_students})
                job_dict.update({'not_interested_students': not_interested_students})
                job_dict.update({'undecided_students': undecided_students})
                student_data_filled = True
        except CompanyInterview.DoesNotExist:
            pass
        if not student_data_filled:
            job_dict.update({'eligible_students': get_students_matching_criteria(job.criteria)})
        jobs.append(job_dict)
    context = {'jobs': jobs, 'company': company_obj}
    return render(request, 'view_student_list.html', context)


def filter_students_for_company(request, company_id):
    jobs_obj = CompanyJob.objects.filter(company_id=company_id)
    jobs = []
    for job in jobs_obj:
        job_dict = {}
        job_dict.update({'name': job.role_name})
        job_dict.update({'eligible_students': get_students_matching_criteria(job.criteria)})
        jobs.append(job_dict)
    return render(request, 'filter_students_for_interview.html', {'jobs': jobs})


def get_students_matching_criteria(criteria):
    min_cgpa = criteria.min_cgpa if criteria.min_cgpa is not None else 0.0
    max_cgpa = criteria.max_cgpa if criteria.max_cgpa is not None else 10.0
    x_min_per = criteria.min_x_percentage if criteria.min_x_percentage is not None else 0.0
    x_max_per = criteria.max_x_percentage if criteria.max_x_percentage is not None else 100.0
    x11_min_per = criteria.min_x11_percentage if criteria.min_x11_percentage is not None else 0.0
    x11_max_per = criteria.max_x11_percentage if criteria.max_x11_percentage is not None else 100.0
    students = StudentAccount.objects.filter(info__batch__in=criteria.get_allowed_batches(),
                                             info__cgpa__gte=min_cgpa,
                                             info__cgpa__lte=max_cgpa,
                                             info__x_percentage__gte=x_min_per,
                                             info__x_percentage__lte=x_max_per,
                                             info__x11_percentage__gte=x11_min_per,
                                             info__x11_percentage__lte=x11_max_per
                                             )
    if criteria.history is not None:
        students = students.filter(info__history_of_backlogs__lte=criteria.history)
    if criteria.current is not None:
        students = students.filter(info__current_backlogs__lte=criteria.current)
    return students

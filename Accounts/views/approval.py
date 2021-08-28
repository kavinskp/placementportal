from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from Accounts.models import StaffAccount, StudentAccount, CustomUser, UserPermissions, UserGroups, InterviewerAccount
from Company.models import CompanyJob


def is_principal(user):
    if user.groups.filter(name=UserGroups.PRINCIPAL.group_name()).exists():
        return True
    return False


def is_hod(user):
    if user.groups.filter(name=UserGroups.HOD.group_name()).exists():
        return True
    return False


def is_faculty(user):
    if user.groups.filter(name=UserGroups.FACULTY.group_name()).exists():
        return True
    return False


def is_po(user):
    if user.groups.filter(name=UserGroups.PLACEMENT_OFFICER.group_name()).exists():
        return True
    return False


def is_pr(user):
    if user.groups.filter(name=UserGroups.PLACEMENT_REPRESENTATIVE.group_name()).exists():
        return True
    return False


def __update_user_approval_status(request):
    return_msg = None
    if 'approve' in request.POST:
        user_list = request.POST.getlist('new_user')
        no_of_users_approved = str(len(user_list))
        for user in user_list:
            appr_user = CustomUser.objects.get(pk=user)
            appr_user.is_approved = True
            appr_user.save()
        return_msg = str('No. of users Approved : ' + no_of_users_approved)
    elif 'de_approve' in request.POST:
        user_list = request.POST.getlist('existing_user')
        no_of_users_de_approved = str(len(user_list))
        for user in user_list:
            de_app_user = CustomUser.objects.get(pk=user)
            de_app_user.is_approved = False
            de_app_user.save()
        return_msg = str('No. of users De-approved : ' + no_of_users_de_approved)
    elif 'delete' in request.POST:
        user_list = request.POST.getlist('new_user')
        no_of_users_deleted = str(len(user_list))
        for user in user_list:
            CustomUser.objects.filter(pk=user).delete()
        return_msg = str('No. of users Deleted : ' + no_of_users_deleted)
    return return_msg


@permission_required(UserPermissions.CAN_APPROVE_STAFF.get_permission())
@user_passes_test(is_principal)
def principal_approval(request):
    values = {'approval_type': 'approve_staff'}
    if request.method == 'POST':
        notification = __update_user_approval_status(request)
        values.update({'notification': [notification]})
    unapproved_users_list = StaffAccount.objects.filter(user__is_approved=False,
                                                        user__user_type=2)
    approved_users_list = StaffAccount.objects.filter(user__is_approved=True,
                                                      user__user_type=2)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@user_passes_test(is_hod)
@permission_required(UserPermissions.CAN_APPROVE_STAFF.get_permission())
def hod_approval(request, user_obj):
    values = {'approval_type': 'approve_staff'}
    if request.method == 'POST':
        notification = __update_user_approval_status(request)
        values.update({'notification': [notification]})

    unapproved_users_list = StaffAccount.objects.filter(user__is_approved=False,
                                                        designation=3,
                                                        department=user_obj.department)
    approved_users_list = StaffAccount.objects.filter(user__is_approved=True, designation=3,
                                                      department=user_obj.department)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@user_passes_test(is_faculty)
def approve_student(request, user_obj):
    values = {'approval_type': 'approve_student'}
    if request.method == 'POST':
        notification = __update_user_approval_status(request)
        values.update({'notification': [notification]})
    unapproved_users_list = StudentAccount.objects.filter(user__is_approved=False,
                                                          info__batch__department=user_obj.department)
    approved_users_list = StudentAccount.objects.filter(user__is_approved=True,
                                                        info__batch__department=user_obj.department)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@user_passes_test(is_po)
def po_company_approvals(request):
    context = {'approval_type': 'approve_interviewer'}
    if request.method == 'POST':
        notification = __update_user_approval_status(request)
        context.update({'notification': [notification]})
    unapproved_users_list = InterviewerAccount.objects.filter(user__is_approved=False)
    approved_users_list = InterviewerAccount.objects.filter(user__is_approved=True)
    context.update({'approved_users_list': approved_users_list})
    context.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', context)


@user_passes_test(is_pr)
def pr_company_approvals(request):
    values = {'approval_type': 'approve_interviewer'}
    if request.method == 'POST':
        notification = __update_user_approval_status(request)
        values.update({'notification': [notification]})
    student_obj = StudentAccount.objects.get(user=request.user)
    jobs = CompanyJob.objects.filter(criteria__batch=student_obj.info.batch)
    company_list = None
    if jobs.exists():
        company_list = jobs.values('company').distinct()
    unapproved_users_list = InterviewerAccount.objects.filter(user__is_approved=False,
                                                              company_info__in=company_list)
    approved_users_list = InterviewerAccount.objects.filter(user__is_approved=True,
                                                            company_info__in=company_list)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@login_required()
@permission_required(UserPermissions.CAN_APPROVE_STAFF.get_permission())
def approve_staff_accounts(request):
    try:
        staff_obj = StaffAccount.objects.get(user=request.user)
        if staff_obj.get_designation_display() == 'Principal':
            return principal_approval(request)
        elif staff_obj.get_designation_display() == 'HOD':
            return hod_approval(request, staff_obj)
        return Http404
    except Exception as e:
        return render(request, 'dashboard/dashboard.html', {
            'error_msg': [str(e)]
        })


@login_required()
@permission_required(UserPermissions.CAN_APPROVE_STUDENT.get_permission())
def approve_student_accounts(request):
    try:
        user_obj = StaffAccount.objects.get(user=request.user)
        return approve_student(request, user_obj)
    except Exception as e:
        return render(request, 'dashboard/dashboard.html', {
            'error_msg': [str(e)]
        })


@login_required()
@permission_required(UserPermissions.CAN_APPROVE_INTERVIEWER.get_permission())
def approve_interviewer_accounts(request):
    try:
        if is_po(user=request.user):
            return po_company_approvals(request)
        if is_pr(user=request.user):
            return pr_company_approvals(request)
    except Exception as e:
        return render(request, 'dashboard/dashboard.html', {
            'error_msg': [str(e)]
        })

from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from Accounts.models import StaffAccount, StudentAccount, CustomUser, UserTypeValue


def can_approve(user):
    if user.has_perm('Accounts.can_allot_hod') or \
            user.has_perm('Accounts.can_approve_faculty') or \
            user.has_perm('Accounts.can_approve_student'):
        return True


@permission_required('Accounts.can_approve_faculty')
def principal_approval(request, user_obj):
    values = {}
    if request.method == 'POST':
        if 'approve' in request.POST:
            user_list = request.POST.getlist('new_user')
            no_of_users_approved = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).update(is_approved=True)
            notify = str('No. of users Approved : ' + no_of_users_approved)
            values.update({'notification': [notify]})
        elif 'de_approve' in request.POST:
            user_list = request.POST.getlist('existing_user')
            no_of_users_de_approved = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).update(is_approved=False)
            notify = str('No. of users De-approved : ' + no_of_users_de_approved)
            values.update({'notification': [notify]})
        elif 'delete' in request.POST:
            user_list = request.POST.getlist('new_user')
            no_of_users_deleted = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).delete()
            notify = str('No. of users Deleted : ' + no_of_users_deleted)
            values.update({'notification': [notify + '  ']})
    unapproved_users_list = StaffAccount.objects.filter(user__is_approved=False, user__user_type=2)
    approved_users_list = StaffAccount.objects.filter(user__is_approved=True, user__user_type=2)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@permission_required('Accounts.can_approve_faculty')
def hod_approval(request, user_obj):
    values = {}
    if request.method == 'POST':
        if 'approve' in request.POST:
            user_list = request.POST.getlist('new_user')
            no_of_users_approved = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).update(is_approved=True)
            notify = str('No. of users Approved : ' + no_of_users_approved)
            values.update({'notification': [notify]})
        elif 'de_approve' in request.POST:
            user_list = request.POST.getlist('existing_user')
            no_of_users_de_approved = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).update(is_approved=False)
            notify = str('No. of users De-approved : ' + no_of_users_de_approved)
            values.update({'notification': [notify]})
        elif 'delete' in request.POST:
            user_list = request.POST.getlist('new_user')
            no_of_users_deleted = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).delete()
            notify = str('No. of users Deleted : ' + no_of_users_deleted)
            values.update({'notification': [notify + '  ']})

    unapproved_users_list = StaffAccount.objects.filter(user__is_approved=False, designation=3,
                                                        department=user_obj.department)
    approved_users_list = StaffAccount.objects.filter(user__is_approved=True, designation=3,
                                                      department=user_obj.department)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@permission_required('Accounts.can_approve_student')
def approve_student(request, user_obj):
    values = {}
    if request.method == 'POST':
        if 'approve' in request.POST:
            user_list = request.POST.getlist('new_user')
            no_of_users_approved = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).update(is_approved=True)
            notify = str('No. of users Approved : ' + no_of_users_approved)
            values.update({'notification': [notify]})
        elif 'de_approve' in request.POST:
            user_list = request.POST.getlist('existing_user')
            no_of_users_de_approved = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).update(is_approved=False)
            notify = str('No. of users De-approved : ' + no_of_users_de_approved)
            values.update({'notification': [notify]})
        elif 'delete' in request.POST:
            user_list = request.POST.getlist('new_user')
            no_of_users_deleted = str(len(user_list))
            for user in user_list:
                CustomUser.objects.filter(email=user).delete()
            notify = str('No. of users Deleted : ' + no_of_users_deleted)
            values.update({'notification': [notify + '  ']})
    unapproved_users_list = StudentAccount.objects.filter(user__is_approved=False, info__department=user_obj.department)
    approved_users_list = StudentAccount.objects.filter(user__is_approved=True, info__department=user_obj.department)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@login_required()
@user_passes_test(can_approve)
def approve_users(request):
    try:
        user_obj = StaffAccount.objects.get(user=request.user)
        if request.user.groups.filter(name='Principal').exists():
            return principal_approval(request, user_obj)
        elif request.user.groups.filter(name='HOD').exists():
            return hod_approval(request, user_obj)
        elif request.user.groups.filter(name='Faculty').exists():
            return approve_student(request, user_obj)
        return Http404
    except Exception as e:
        return render(request, 'dashboard.html', {
            'error_msg': [str(e)]
        })

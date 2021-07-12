from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from Accounts.models import Staff, Student, CustomUser


def can_approve(user):
    if user.has_perm('Accounts.can_allot_hod') or \
            user.has_perm('Accounts.can_approve_faculty') or \
            user.has_perm('Accounts.can_approve_student'):
        return True


@permission_required('Accounts.can_allot_hod')
def approve_hod(request, user_obj):
    values = {
        'approval_type': 'hod',
        'user_obj': user_obj,
    }
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
    unapproved_users_list = Staff.objects.filter(user__is_approved=False, designation=2)
    approved_users_list = Staff.objects.filter(user__is_approved=True, designation=2)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    print(unapproved_users_list)
    return render(request, 'approval.html', values)


@permission_required('Accounts.can_approve_faculty')
def approve_faculty(request, user_obj):
    print(user_obj)
    values = {
        'approval_type': 'faculty',
        'user_obj': user_obj,
    }
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
    unapproved_users_list = Staff.objects.filter(user__is_approved=False, designation=3, department=user_obj.department)
    approved_users_list = Staff.objects.filter(user__is_approved=True, designation=3, department=user_obj.department)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@permission_required('Accounts.can_approve_student')
def approve_student(request, user_obj):
    values = {
        'approval_type': 'student',
        'user_obj': user_obj,
    }
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
    unapproved_users_list = Student.objects.filter(user__is_approved=False, department=user_obj.department)
    approved_users_list = Student.objects.filter(user__is_approved=True, department=user_obj.department)
    values.update({'approved_users_list': approved_users_list})
    values.update({'unapproved_users_list': unapproved_users_list})
    return render(request, 'approval.html', values)


@login_required()
@user_passes_test(can_approve)
def approve_users(request):
    if request.session is not None:
        try:
            is_staff_acc = bool(request.session.get('is_staff_acc'))
            if is_staff_acc:
                user_obj = Staff.objects.get(user=request.user)
            else:
                raise PermissionError('You don\'t have permission')
            user_type = request.session.get('user_type')
            print(user_type)
            if user_type == 'Principal':
                return approve_hod(request, user_obj)
            elif user_type == 'HOD':
                return approve_faculty(request, user_obj)
            elif user_type == 'Faculty':
                return approve_student(request, user_obj)
            return Http404
        except PermissionError:
            msg = {
                'page_title': 'Placement | Permission Denied',
                'title': 'Not Approved',
                'description': ['User doesn\'t have permission!']
            }
            return render(request, 'prompt_pages.html', {'message': msg})
    return redirect('login')

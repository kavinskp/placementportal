from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404
from django.contrib import messages

from Curriculum.forms import BatchForm
from Curriculum.models import Regulation, Department, Batch
from Accounts.models import UserPermissions
from Accounts.views.utils import *


@permission_required(UserPermissions.CAN_UPDATE_BATCHES.get_permission())
def update_batches(request, batches):
    is_error = False
    form = None
    error_msg = None
    try:
        form = BatchForm(request.POST)
        if form.is_valid():
            batch_obj = form.save()
            msg = "Created batch " + str(batch_obj) + " !"
            messages.success(request, msg)
            return redirect('view_batches')
        else:
            is_error = True
            error_msg = ['Validation Failure!']
    except forms.ValidationError as error:
        error_msg = [error]
        is_error = True
    if is_error:
        return render(request, 'view_batches.html', {
            'batches': batches,
            'form': form,
            'error_msg': error_msg
        })


def view_batches(request):
    error_msg = None
    batches = Batch.objects.all()
    if request.method == 'POST':
       return update_batches(request, batches)
    form = BatchForm()
    return render(request, 'view_batches.html', {
        'batches': batches,
        'form': form,
        'error_msg': error_msg
    })


@permission_required(UserPermissions.CAN_UPDATE_BATCHES.get_permission())
def delete_batch(request, batch_id):
    batch_obj = Batch.objects.get(pk=batch_id)
    batch_obj.in_active = True
    batch_obj.save()
    msg = "Batch " + str(batch_obj) + " for Department " + str(batch_obj.department) + " marked as Inactive !"
    messages.success(request, msg)
    return redirect('view_batches')


@permission_required(UserPermissions.CAN_ASSIGN_HOD.get_permission())
def assign_hod(request):
    if request.method == 'POST':
        dep_name = request.POST['dep_name']
        staff_id = request.POST['staff_id']
        try:
            if staff_id is not None:
                staff_obj = getStaffUsingStaffId(staff_id)
                staff_obj.designation = 2
                staff_obj.save()
                user_obj = staff_obj.user
                group = Group.objects.get(name='HOD')
                group.user_set.add(user_obj)
                msg = staff_obj.full_name() + " alloted as HOD of " + dep_name + "!"
                messages.success(request, msg)
                return redirect('view_hods')
        except Exception as e:
            return render(request, 'dashboard.html', {
                'error_msg': [str(e)]
            })


def view_hods(request):
    error_msg = None
    hods = getHODsOrderByName()
    if request.method == 'POST':
       return assign_hod(request)
    departments = Department.objects.all().exclude(name='General')
    return render(request, 'view_hods_info.html', {
        'hods_info': hods,
        'departments': departments,
        'error_msg': error_msg
    })


def load_faculties(request):
    dep_name = request.GET.get('dep_name')
    staffs = getFacultiesOrderByName(dep_name=dep_name)
    return render(request, 'set_object_list_as_options.html', {
        'options': staffs,
    })


def load_staffs(request):
    dep_name = request.GET.get('dep_name')
    staffs = getStaffsOrderByName(dep_name=dep_name)
    return render(request, 'set_object_list_as_options.html', {
        'options': staffs,
    })


@permission_required(UserPermissions.CAN_ASSIGN_HOD.get_permission())
def un_assign_hod(request, staff_id):
    staff_obj = getStaffUsingStaffId(staff_id)
    staff_obj.designation = 3
    staff_obj.save()
    user_obj = staff_obj.user
    group = Group.objects.get(name='HOD')
    group.user_set.remove(user_obj)
    msg = str(staff_obj.full_name()) + " removed from HOD of " + str(staff_obj.department) + "!"
    messages.success(request, msg)
    return redirect('view_hods')


@permission_required(UserPermissions.CAN_ASSIGN_PO.get_permission())
def assign_po(request):
    staff_id = request.POST['staff_id']
    try:
        if staff_id is not None:
            staff_obj = getStaffUsingStaffId(staff_id)
            user_obj = staff_obj.user
            group = Group.objects.get(name='PO')
            group.user_set.add(user_obj)
            msg = staff_obj.full_name() + " assigned as Placement Officer"
            messages.success(request, msg)
            return redirect('view_po_details')
    except Exception as e:
        return render(request, 'dashboard.html', {
            'error_msg': [str(e)]
        })


def view_po_details(request):
    error_msg = None
    if request.method == 'POST':
        return assign_po(request)
    departments = Department.objects.all()
    pos = getPlacementOfficers()
    return render(request, 'view_placement_officer_details.html', {
        'pos_info': pos,
        'departments': departments,
        'error_msg': error_msg
    })


@permission_required(UserPermissions.CAN_ASSIGN_PO.get_permission())
def un_assign_po(request, staff_id):
    staff_obj = getStaffUsingStaffId(staff_id)
    user_obj = staff_obj.user
    group = Group.objects.get(name='PO')
    group.user_set.remove(user_obj)
    msg = staff_obj.full_name() + " removed from Placement Officer Role"
    messages.success(request, msg)
    return redirect('view_po_details')


def view_all_pr_details(request):
    batches = Regulation.objects.all()
    prs = getAllPlacementRepresentatives()
    return render(request, 'view_pr_details.html', {
        'batches': batches,
        'prs_info': prs,
    })


@permission_required(UserPermissions.CAN_ASSIGN_PR.get_permission())
def assign_pr(request):
    staff_obj = StaffAccount.objects.get(user=request.user)
    dep_name = staff_obj.department
    error_msg = None
    if request.method == 'POST':
        roll_no = request.POST['roll_no']
        try:
            if roll_no is not None:
                student_obj = getStudentByRollNO(roll_no)
                user_obj = student_obj.user
                group = Group.objects.get(name='PR')
                group.user_set.add(user_obj)
                msg = student_obj.full_name() + " alloted as PR for " + str(dep_name) + "!"
                messages.success(request, msg)
                return redirect('assign_pr')
        except Exception as e:
            error_msg = [str(e)]
    batches = Batch.objects.filter(department__name=dep_name)
    prs_info = getAllPlacementRepresentatives(dep_name=dep_name)
    return render(request, 'assign_pr_for_batch.html', {
        'prs_info': prs_info,
        'dep_name': dep_name,
        'batches': batches,
        'error_msg': error_msg
    })


@permission_required(UserPermissions.CAN_ASSIGN_PR.get_permission())
def un_assign_pr(request, roll_no):
    student_obj = getStudentByRollNO(roll_no)
    user_obj = student_obj.user
    group = Group.objects.get(name='PR')
    group.user_set.remove(user_obj)
    msg = student_obj.full_name() + " removed from Placement Representative"
    messages.success(request, msg)
    return redirect('assign_pr')


def load_students_for_given_dep_batch(request):
    batch_id = request.GET.get('batch_id')
    students = getAllBatchStudentsSortByName(batch_id)
    return render(request, 'set_object_list_as_options.html', {
        'options': students,
    })

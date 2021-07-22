from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.contrib import messages

from Curriculum.forms import BatchForm
from Curriculum.models import Regulation, Department, Batch
from Accounts.views.utils import *


def view_batches(request):
    error_msg = None
    form = None
    batches = Batch.objects.all()
    if request.method == 'POST':
        is_error = False
        try:
            form = BatchForm(request.POST)
            if form.is_valid():
                form.save()
                msg = "Created batch !"
                messages.success(request, msg)
                return redirect('view_batches')
            else:
                is_error = True
        except forms.ValidationError as error:
            error_msg = [error]
            is_error = True
        if is_error:
            return render(request, 'view_batches.html', {
                'batches': batches,
                'form': form,
                'error_msg': error_msg
            })
    form = BatchForm()
    return render(request, 'view_batches.html', {
        'batches': batches,
        'form': form,
        'error_msg': error_msg
    })


@permission_required('Curriculam.can_update_batches')
def delete_batch(request, batch_id):
    batch_obj = Batch.objects.get(pk=batch_id)
    batch_obj.delete()
    msg = "Removed batch " + str(batch_obj) + " for Department " + str(batch_obj.department) + " !"
    messages.success(request, msg)
    return redirect('view_batches')


@permission_required('Accounts.can_allot_hod')
def list_hods(request):
    hods = getHODsOrderByName()
    return render(request, 'view_hods_info.html', {
        'hods_info': hods,
    })


@permission_required('Accounts.can_allot_hod')
def assign_hod(request):
    error_msg = None
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
                return redirect('list_hods_info')
        except:
            error_msg = ["Update Failed!!"]
    departments = Department.objects.all().exclude(name='General')
    return render(request, 'allot_hod.html', {
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


@permission_required('Accounts.can_allot_hod')
def un_assign_hod(request, staff_id):
    staff_obj = getStaffUsingStaffId(staff_id)
    staff_obj.designation = 3
    staff_obj.save()
    user_obj = staff_obj.user
    group = Group.objects.get(name='HOD')
    group.user_set.remove(user_obj)
    msg = staff_obj.full_name() + " removed from HOD of " + staff_obj.department.name + "!"
    messages.success(request, msg)
    return redirect('list_hods_info')


def view_po_details(request):
    error_msg = None
    if request.method == 'POST':
        staff_id = request.POST['staff_id']
        try:
            if staff_id is not None:
                staff_obj = getStaffUsingStaffId(staff_id)
                user_obj = staff_obj.user
                group = Group.objects.get(name='PO')
                group.user_set.add(user_obj)
                msg = staff_obj.full_name() + " assigned as Placement Officer"
                messages.success(request, msg)
                return redirect('view_po')
        except:
            error_msg = ["Update Failed!!"]
    departments = Department.objects.all()
    pos = getPlacementOfficers()
    return render(request, 'view_placement_officer_details.html', {
        'pos_info': pos,
        'departments': departments,
        'error_msg': error_msg
    })


@permission_required('Accounts.can_assign_po')
def un_assign_po(request, staff_id):
    staff_obj = getStaffUsingStaffId(staff_id)
    user_obj = staff_obj.user
    group = Group.objects.get(name='PO')
    group.user_set.remove(user_obj)
    msg = staff_obj.full_name() + " removed from Placement Officer Role"
    messages.success(request, msg)
    return redirect('view_po')


def view_all_pr_details(request):
    batches = Regulation.objects.all()
    prs = getAllDepartmentPRs()
    return render(request, 'view_pr_details.html', {
        'batches': batches,
        'prs_info': prs,
    })


@permission_required('Accounts.can_assign_pr')
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
                msg = student_obj.full_name() + " alloted as PR for " + dep_name + "!"
                messages.success(request, msg)
                return redirect('list_hods_info')
        except:
            error_msg = ["Update Failed!!"]
    batches = Batch.objects.filter(department__name=dep_name)
    prs_info = getPlacementRepresentatives(dep_name=dep_name)
    return render(request, 'assign_pr_for_batch.html', {
        'prs_info': prs_info,
        'dep_name': dep_name,
        'batches': batches,
        'error_msg': error_msg
    })


@permission_required('Accounts.can_assign_pr')
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
    dep_name = request.GET.get('dep_name')
    students = getAllStudentsSortByName(dep_name).filter(info__batch__pk=batch_id)
    return render(request, 'set_object_list_as_options.html', {
        'options': students,
    })

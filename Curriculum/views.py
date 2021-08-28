from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from Curriculum.forms import BatchForm, RegulationForm, UpdateRegulationForm
from Accounts.models import UserPermissions
from Accounts.views.utils import *


def view_batches(request):
    batch_form = BatchForm()
    active_batches = Batch.objects.filter(active=True)
    inactive_batches = Batch.objects.filter(active=False)
    error_msg = None
    if request.method == 'POST':
        if request.user.has_perm(UserPermissions.CAN_UPDATE_BATCHES.get_permission()):
            try:
                if 'create_batch' in request.POST:
                    batch_form = BatchForm(request.POST)
                    if batch_form.is_valid():
                        batch_obj = batch_form.save()
                        msg = "Created batch " + str(batch_obj) + " !"
                        messages.success(request, msg)
                        return redirect('view_batches')
                    else:
                        error_msg = ['Cannot create batch']
                        if batch_form.errors is not None:
                            error_msg = []
                            for error in batch_form.non_field_errors():
                                error_msg.append(error)
            except forms.ValidationError as e:
                error_msg = [str(e)]
        else:
            error_msg = ['You don\'t have permission to do this action']
    return render(request, 'view_batches.html', {
        'batches': active_batches,
        'inactive_batches': inactive_batches,
        'batch_form': batch_form,
        'error_msg': error_msg
    })


def view_regulations(request):
    regulations = Regulation.objects.filter(active=True)
    inactive_regulations = Regulation.objects.filter(active=False)
    regulation_form = RegulationForm()
    error_msg = None
    if request.method == 'POST':
        if request.user.has_perm(UserPermissions.CAN_UPDATE_BATCHES.get_permission()):
            if 'create_regulation' in request.POST:
                regulation_form = RegulationForm(request.POST)
                if regulation_form.is_valid():
                    reg_obj = regulation_form.save()
                    msg = "Created Regulation " + str(reg_obj) + " !"
                    messages.success(request, msg)
                    return redirect('view_regulations')
                else:
                    error_msg = ['Cannot create regulation']
                    if regulation_form.errors is not None:
                        error_msg = []
                        for error in regulation_form.non_field_errors():
                            error_msg.append(error)
            elif 'update_current_semester' in request.POST:
                try:
                    regulation_id = request.POST['regulation_id']
                    regulation = Regulation.objects.get(pk=regulation_id)
                    current_sem = int(request.POST['current_semester'])
                    programme_period = regulation.programme_period
                    if current_sem > programme_period * 2:
                        raise forms.ValidationError(
                            'Cannot be greater than ' + str(programme_period * 2) + " for this regulation!")
                    prev_reg_objs = Regulation.objects.filter(programme=regulation.programme,
                                                              start_year__gt=regulation.start_year,
                                                              current_semester__lt=current_sem,
                                                              current_semester__gt=0)
                    if prev_reg_objs.exists():
                        raise forms.ValidationError(
                            'Current semester cannot be greater than regulations started before!')
                    prev_reg_objs = Regulation.objects.filter(programme=regulation.programme,
                                                              start_year__lt=regulation.start_year,
                                                              current_semester__gt=current_sem)
                    if prev_reg_objs.exists():
                        raise forms.ValidationError(
                            'Current semester cannot be lesser than regulations started after!')
                    reg_objs = Regulation.objects.filter(programme=regulation.programme,
                                                         current_semester=current_sem).exclude(
                        start_year=regulation.start_year)
                    if reg_objs.exists():
                        raise forms.ValidationError(
                            'Another regulation started in different year in this programme has same value!')
                    regulation.current_semester = current_sem
                    regulation.save()
                    msg = "Current semester for regulation " + str(regulation) + " is updated! "
                    messages.success(request, msg)
                    return redirect('view_regulations')
                except forms.ValidationError as e:
                    error_msg = e
        else:
            error_msg = ['You don\'t have permission to do this action']
    return render(request, 'view_regulations.html', {
        'regulations': regulations,
        'inactive_regulations': inactive_regulations,
        'regulation_form': regulation_form,
        'error_msg': error_msg
    })


def ajax_load_regulation_form(request):
    regulation_id = request.GET.get('regulation_id')
    regulation_obj = Regulation.objects.get(pk=regulation_id)
    form = UpdateRegulationForm(instance=regulation_obj)
    cancel_url = redirect('view_regulations')
    return render(request, 'ajax_load_form_in_card.html', {
        'form': form,
        'id': regulation_id,
        'form_title': 'Edit Regulation Information',
        'submit_name': 'update_regulation',
        'cancel_url': cancel_url
    })


@permission_required(UserPermissions.CAN_UPDATE_BATCHES.get_permission())
def mark_as_active_batch(request, batch_id):
    batch_obj = Batch.objects.get(pk=batch_id)
    batch_obj.active = True
    batch_obj.save()
    msg = str(batch_obj) + " batch marked as active !"
    messages.success(request, msg)
    return redirect('view_batches')


@permission_required(UserPermissions.CAN_UPDATE_BATCHES.get_permission())
def delete_regulation(request, regulation_id):
    if request.method == 'POST':
        if 'delete' in request.POST:
            regulation_id = request.POST['id']
            regulation_obj = Regulation.objects.get(pk=regulation_id)
            regulation_obj.delete()
            msg = "Regulation " + str(regulation_obj) + " is deleted !"
            messages.success(request, msg)
            return redirect('view_batches')
        if 'mark_as_inactive' in request.POST:
            regulation_id = request.POST['id']
            regulation_obj = Regulation.objects.get(pk=regulation_id)
            batch_objs = Batch.objects.filter(regulation=regulation_obj)
            for batch_obj in batch_objs:
                batch_obj.active = False
                batch_obj.save()
            regulation_obj.active = False
            regulation_obj.save()
            msg = str(len(batch_objs)) + " batches marked as inactive !"
            messages.success(request, msg)
            return redirect('view_batches')
    regulation_obj = Regulation.objects.get(pk=regulation_id)
    batches = Batch.objects.filter(regulation=regulation_obj)
    students = StudentAccount.objects.filter(info__batch__regulation=regulation_obj)
    confirm_text = str(len(students)) + ' students is in this regulation ' + str(
        regulation_obj) + ' !! Please check and confirm!'
    return render(request, 'check_and_delete_batch.html', {
        'id': regulation_id,
        'batches': batches,
        'students': students,
        'confirm_text': confirm_text
    })


@permission_required(UserPermissions.CAN_UPDATE_BATCHES.get_permission())
def delete_batch(request, batch_id):
    if request.method == 'POST':
        if 'delete' in request.POST:
            batch_id = request.POST['id']
            batch_obj = Batch.objects.get(pk=batch_id)
            batch_obj.delete()
            msg = "Batch " + str(batch_obj) + " for Department " + str(batch_obj.department) + " is deleted !"
            messages.success(request, msg)
            return redirect('view_batches')
        if 'mark_as_inactive' in request.POST:
            batch_id = request.POST['id']
            batch_obj = Batch.objects.get(pk=batch_id)
            batch_obj.active = False
            batch_obj.save()
            msg = "Batch " + str(batch_obj) + " for Department " + str(
                batch_obj.department) + " is marked as inactive !"
            messages.success(request, msg)
            return redirect('view_batches')
    batch_obj = Batch.objects.get(pk=batch_id)
    students = StudentAccount.objects.filter(info__batch_id=batch_id)
    confirm_text = str(len(students)) + ' students is in batch ' + str(batch_obj) + ' !! Please check and confirm!'
    return render(request, 'check_and_delete_batch.html', {
        'id': batch_id,
        'students': students,
        'confirm_text': confirm_text
    })


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
            msg = str(e)
            messages.error(request, msg)
            return redirect('dashboard')


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
        msg = str(e)
        messages.error(request, msg)
        return redirect('dashboard')


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
                msg = student_obj.full_name() + " alloted as PR for " + str(student_obj.batch()) + "!"
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

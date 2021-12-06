from django import forms
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from Accounts.models import InterviewerAccount
from Accounts.views.utils import create_interviewer_account
from .forms import CompanyInfoForm, HRContactInfoForm, RoleInfoForm, JobCriteriaForm, RoundInfoForm
from .models import CompanyInfo, CompanyJob, HRContactInfo, Criteria, RoundInfo, PreferenceSchedulePeriod
from Curriculum.models import Batch


def get_context(title, form, form_type, error, alert=None):
    return {
        'form': form,
        'title': title,
        'form_type': form_type,
        'error_msg': error,
        'alert': alert
    }


HR_INFO = 'hr_info'
COMPANY_INFO = 'company_info'
JOB_INFO = 'job_info'


def add_hr_info(request, company_id=None):
    error = None
    curr_form = HR_INFO
    form = None
    title = 'Interviewer Contact Details'
    current_user_not_added = True
    if request.method == 'POST':
        if 'submit' in request.POST or 'save_and_add' in request.POST:
            form = HRContactInfoForm(request.POST)
            try:
                if form.is_valid():
                    hr = form.save(commit=False)
                    hr.company = CompanyInfo.objects.get(pk=company_id)
                    hr.save()
                    if 'save_and_add' in request.POST:
                        return redirect('add_hr_info', company_id=company_id)
                    else:
                        return redirect('create_roles', company_id=company_id)
                else:
                    error = ["Please Enter correct Details!!"]
            except forms.ValidationError as e:
                error = [str(e)]
    else:
        form = HRContactInfoForm()
    existing_recruiters = HRContactInfo.objects.filter(company_id=company_id)
    user_name = None
    if request.session is not None:
        user_name = request.session.get('user_name')
        if HRContactInfo.objects.filter(company_id=company_id, email=user_name).exists():
            current_user_not_added = False
    else:
        current_user_not_added = False
    context = get_context(title, form, curr_form, error)
    context.update({'user_name': user_name})
    context.update({'company_id': company_id})
    context.update({'existing_recruiters': existing_recruiters})
    context.update({'current_user_not_added': current_user_not_added})

    return render(request, 'register_company.html', context)


def delete_recruiter(request, company_id, recruiter_id):
    hr = HRContactInfo.objects.get(pk=recruiter_id)
    hr.delete()
    msg = "Recruiter " + str(hr.full_name()) + " removed !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('add_hr_info', company_id)


def add_recuiter(request, company_id):
    if request.method == 'POST':
        form = HRContactInfoForm(request.POST)
        try:
            if form.is_valid():
                hr = form.save(commit=False)
                hr.company = CompanyInfo.objects.get(pk=company_id)
                hr.save()
                msg = "Recruiter " + str(hr.full_name()) + " added !"
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                messages.success(request, msg)
                return redirect('add_hr_info', company_id=company_id)
            else:
                error = ["Please Enter correct Details!!"]
        except forms.ValidationError as e:
            error = [str(e)]
    else:
        form = HRContactInfoForm()
    return redirect('ajax_load_regulation_form', company_id)


def create_roles(request, company_id):
    error = None
    curr_form = JOB_INFO
    form = None
    company_info = CompanyInfo.objects.get(pk=company_id)
    create_role_form = RoleInfoForm(company_id=company_id)
    create_criteria_form = JobCriteriaForm()
    title = 'Job Details'
    if request.method == 'POST':
        try:
            if 'create_criteria' in request.POST:
                criteria_form = JobCriteriaForm(request.POST, request.FILES)
                if criteria_form.is_valid():
                    criteria = criteria_form.save(commit=False)
                    criteria.company = company_info
                    criteria.save()
                    batches = request.POST.getlist('batch')
                    for batch_id in batches:
                        criteria.batch.add(Batch.objects.get(id=batch_id))

            if 'create_role' in request.POST:
                create_role_form = RoleInfoForm(request.POST, request.FILES, company_id=company_id)
                if create_role_form.is_valid():
                    role_obj = create_role_form.save(commit=False)
                    role_obj.company = company_info
                    role_obj.save()
            if 'complete' in request.POST:
                if not CompanyJob.objects.filter(company=company_info).exists():
                    error = ["At least one job role must be defined !"]
                else:
                    msg = "Company Details saved !"
                    messages.success(request, msg)
                    if request.user.is_authenticated():
                        return redirect('create_roles', company_id)
                    return redirect('dashboard')
        except Exception as e:
            error = [str(e)]
    existing_criteria = Criteria.objects.filter(company_id=company_id)
    existing_roles = CompanyJob.objects.filter(company_id=company_id)
    context = get_context(title, form, curr_form, error)
    context.update({'company_id': company_id})
    context.update({'create_role_form': create_role_form})
    context.update({'create_criteria_form': create_criteria_form})
    context.update({'existing_roles': existing_roles})
    context.update({'existing_criteria': existing_criteria})
    return render(request, 'create_roles.html', context)


def update_role(request, company_id, role_id):
    error = None
    role = CompanyJob.objects.get(pk=role_id)
    title = 'Update Role - ' + role.role_name
    if request.method == 'POST':
        try:
            if 'update_role' in request.POST:
                form = RoleInfoForm(request.POST, request.FILES, instance=role, company_id=company_id)
                if form.is_valid():
                    form.save()
                    msg = "Role " + str(role.role_name) + " saved !"
                    messages.success(request, msg)
                    if request.user.is_authenticated():
                        return redirect('create_roles', company_id)
                    return redirect('dashboard')
        except Exception as e:
            error = [str(e)]
    form = RoleInfoForm(instance=role, company_id=company_id)
    return render(request, 'edit_role_info.html', {
        'form': form,
        'title': title,
        'error_msg': error,
        'company_id': company_id
    })


def ajax_get_criteria_for_company(request):
    company_id = request.GET.get('company_id')
    criteria = Criteria.objects.filter(company_id=company_id)
    return render(request, 'load_objects_as_options.html', {
        'options': criteria,
    })


def delete_role(request, company_id, role_id):
    CompanyJob.objects.get(pk=role_id).delete()
    return redirect('create_roles', company_id)


def delete_criteria(request, company_id, criteria_id):
    Criteria.objects.get(pk=criteria_id).delete()
    return redirect('create_roles', company_id)


def edit_criteria(request, company_id, criteria_id):
    error = None
    criteria = Criteria.objects.get(pk=criteria_id)
    title = 'Update criteria - ' + criteria.name
    if request.method == 'POST':
        try:
            if 'edit_criteria' in request.POST:
                form = JobCriteriaForm(request.POST, request.FILES, instance=criteria)
                if form.is_valid():
                    form.save()
                    msg = "Role " + str(criteria.name) + " saved !"
                    messages.success(request, msg)
                    if request.user.is_authenticated():
                        return redirect('create_roles', company_id)
                    return redirect('dashboard')
        except Exception as e:
            error = [str(e)]
    form = JobCriteriaForm(instance=criteria)
    return render(request, 'edit_criteria.html', {
        'form': form,
        'title': title,
        'error_msg': error,
        'company_id': company_id
    })


def preview_role_document(request, role_id):
    role = CompanyJob.objects.get(pk=role_id)
    return preview_document(role.documents, filename=role.documents)


def preview_document(request, filename):
    try:
        return FileResponse(open(filename, 'rb'))
    except FileNotFoundError:
        messages.error(request, "File not exist")
        return redirect('index')


def register_company(request):
    error = None
    curr_form = COMPANY_INFO
    title = 'Company Details'
    form = CompanyInfoForm()
    update = False
    company_info = None
    interviewer_obj = None
    user_name = None
    if request.session is not None:
        user_name = request.session.get('user_name')
        if user_name is not None:
            if InterviewerAccount.objects.filter(user__email=user_name).exists():
                interviewer_obj = InterviewerAccount.objects.get(user__email=user_name)
                company_info = interviewer_obj.company_info
                update = True
    if request.method == 'POST':
        if 'submit' in request.POST:
            try:
                if update:
                    form = CompanyInfoForm(request.POST, request.FILES, instance=company_info)
                else:
                    form = CompanyInfoForm(request.POST, request.FILES)
                if form.is_valid():
                    company_info = form.save()
                    if interviewer_obj:
                        interviewer_obj.company_info = company_info
                        interviewer_obj.save()
                    elif user_name:
                        create_interviewer_account(request.user, company_info)
                    return redirect('add_hr_info', company_id=company_info.pk)
                else:
                    print(form.errors)
                    error = ["Please Enter correct Details!!"]
            except Exception as e:
                error = [str(e)]
    else:
        if update:
            form = CompanyInfoForm(instance=company_info)
        else:
            form = CompanyInfoForm()
    context = get_context(title, form, curr_form, error)
    return render(request, 'register_company.html', context)


def ajax_load_company_details(request):
    company_id = request.GET.get('company_id')
    company_info = CompanyInfo.objects.get(pk=company_id)
    jobs = CompanyJob.objects.filter(company_id=company_id)
    return render(request, 'ajax_load_company_job_info_in_table.html', {
        'company_info': company_info,
        'jobs': jobs
    })


def ajax_get_allowed_batches_for_job(request):
    criteria_id = request.GET.get('job_id')
    criteria = Criteria.objects.get(pk=criteria_id)
    return criteria.get_allowed_batch_html()


def ajax_load_round_info_form(request):
    round_id = request.GET.get('round_info_id', None)
    if round_id is None:
        company_id = request.GET.get('company_id')
        form = RoundInfoForm()
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/view_company_info/' + str(company_id) + '/',
            'submit_name': 'add_round_info',
        })
    else:
        entry = get_object_or_404(RoundInfo, pk=round_id)
        form = RoundInfoForm(instance=entry)
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/view_company_info/' + str(entry.company_id) + '/',
            'submit_name': 'edit_round_info',
            'id': round_id
        })


def delete_round_info(request, round_info_id):
    round = RoundInfo.objects.get(pk=round_info_id)
    company_id = round.company_id
    round.delete()
    msg = "Removed Round - " + str(round) + " !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('view_company_info', company_id)


def view_company_info(request, company_id):
    company_info = CompanyInfo.objects.get(pk=company_id)
    error = None
    if request.method == 'POST':
        if 'edit_recruiter' in request.POST:
            recruiter_id = request.POST['id']
            entry = get_object_or_404(HRContactInfo, pk=recruiter_id)
            hr_form = HRContactInfoForm(request.POST, instance=entry)
            try:
                if hr_form.is_valid():
                    hr = hr_form.save()
                    msg = "Recruiter " + str(hr.full_name()) + " information saved !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if hr_form.errors is not None:
                        error = []
                        for err in hr_form.errors:
                            for er in hr_form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
        elif 'edit_round_info' in request.POST:
            round_id = request.POST['id']
            entry = get_object_or_404(RoundInfo, pk=round_id)
            round_form = RoundInfoForm(request.POST, instance=entry)
            try:
                if round_form.is_valid():
                    round_info = round_form.save()
                    msg = "Round " + str(round_info) + " information saved !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if round_form.errors is not None:
                        error = []
                        for err in round_form.errors:
                            for er in round_form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
        elif 'add_round_info' in request.POST:
            round_form = RoundInfoForm(request.POST)
            try:
                if round_form.is_valid():
                    round_info = round_form.save(commit=False)
                    round_info.company = company_info
                    round_info.save()
                    msg = "Round " + str(round_info) + " create for company " + str(round_info.company) + "!"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if round_form.errors is not None:
                        error = []
                        for err in round_form.errors:
                            for er in round_form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
        else:
            hr_form = HRContactInfoForm(request.POST)
            try:
                if hr_form.is_valid():
                    hr = hr_form.save(commit=False)
                    hr.company = company_info
                    hr.save()
                    msg = "Recruiter " + str(hr.full_name()) + " added !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if hr_form.errors:
                        error = []
                        for err in hr_form.errors:
                            for er in hr_form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
    hr_form = HRContactInfoForm()
    return render(request, 'view_company_info.html',
                  {'company_info': company_info, 'form': hr_form, 'error_msg': error})

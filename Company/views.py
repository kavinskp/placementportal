from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateCompanyInfo, CreateHRContactInfo
from .models import Company
from django import forms


def getContext(title, form, form_type, error, alert=None):
    return {
        'form': form,
        'title': title,
        'form_type': form_type,
        'error_msg': error,
        'alert': alert
    }


HR_INFO = 'hr_info'
COMPANY_INFO = 'company_info'


def add_hr_info(request, company_id=None):
    error = None
    curr_form = HR_INFO
    form = None
    title = 'Interviewer Contact Details'
    if request.method == 'POST':
        if 'submit' in request.POST or 'save_and_add' in request.POST:
            form = CreateHRContactInfo(request.POST)
            try:
                if form.is_valid():
                    hr = form.save(commit=False)
                    hr.company = Company.objects.get(pk=company_id)
                    hr.save()
                    if 'save_and_add' in request.POST:
                        return redirect('add_hr_info', company_id=company_id)
                    else:
                        msg = {
                            'page_title': 'Register Company',
                            'title': 'Add company - Success',
                            'description': ["Company Details Added Successfully"]
                        }
                    return render(request, 'prompt_pages.html', {'message': msg})
                else:
                    print(form.errors)
                    error = ["Please Enter correct Details!!"]
            except forms.ValidationError as e:
                error = [str(e)]
    else:
        form = CreateHRContactInfo()
    context = getContext(title, form, curr_form, error)
    return render(request, 'crf.html', context)


# def edit_company_info(request, company_id):
#     error = None
#     curr_form = COMPANY_INFO
#     if request.method == 'POST':
#         try:
#             if 'submit' in request.POST:
#                 form = CreateCompanyInfo(request.POST)
#                 if form.is_valid():
#                     company = form.save()
#                     form.save()
#                     return redirect('hr_info', company_id=company.pk)
#         except Exception as e:
#             error = [str(e)]
#     form = CreateCompanyInfo()
#     if company_id is not None:
#         company = get_object_or_404(Company, pk=company_id)
#         form = CreateCompanyInfo(None, instance=company)
#     title = 'Company Details'
#     print(title)
#     print(company_id)
#     context = getContext(title, form, curr_form, error)
#     return render(request, 'crf.html', context)


def register_company(request):
    error = None
    curr_form = COMPANY_INFO
    title = 'Company Details'
    form = None
    if request.method == 'POST':
        if 'submit' in request.POST:
            try:
                print(request.POST)
                form = CreateCompanyInfo(request.POST, request.FILES)
                if form.is_valid():
                    company = form.save()
                    return redirect('add_hr_info', company_id=company.pk)
                else:
                    print(form.errors)
                    error = ["Please Enter correct Details!!"]
            except Exception as e:
                error = [str(e)]
    else:
        form = CreateCompanyInfo()
    context = getContext(title, form, curr_form, error)
    return render(request, 'crf.html', context)


def crf(request):
    return redirect('register_company')

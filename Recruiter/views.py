import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django import forms
from Company.models import CompanyInfo, HRContactInfo
from Company.forms import CompanyInfoForm, HRContactInfoForm


def view_company_info(request):
    return render(request, '')


def ajax_load_edit_company_form(request, company_id):
    company_info = CompanyInfo.objects.get(pk=company_id)
    form = CompanyInfoForm(instance=company_info)
    return render(request, 'ajax_load_form_in_card.html', {
        'form': form,
        'form_title': 'Edit Company Information',
    })


def ajax_load_edit_recruiter_form(request):
    recruiter_id = request.GET['recruiter_id']
    entry = get_object_or_404(HRContactInfo, pk=recruiter_id)
    form = HRContactInfoForm(instance=entry)
    return render(request, 'ajax_load_form_in_div.html', {
        'form': form,
        'action_url': '/view_company_info/' + str(entry.company_id) + '/',
        'submit_name': 'edit_recruiter',
        'id': recruiter_id
    })


def ajax_add_recruiter(request, company_id):
    error = None
    if request.method == 'POST':
        hr_form = HRContactInfoForm(request.POST)
        try:
            if hr_form.is_valid():
                hr = hr_form.save(commit=False)
                hr.company = CompanyInfo.objects.get(pk=company_id)
                hr.save()
                msg = "Recruiter " + str(hr.full_name()) + " added !"
                messages.success(request, msg)
            else:
                if hr_form.errors:
                    error = {}
                    for err in hr_form.errors:
                        error_ms = []
                        for er in hr_form.errors.get(err):
                            error_ms.append(er)
                        error.update({err: str.join(' ', error_ms)})
        except forms.ValidationError as e:
            error = [str(e)]
    if error:
        response = HttpResponse(
            json.dumps(error),
            content_type='application/javascript; charset=utf8'
        )
        response.status_code = 403
        return response
    else:
        response = HttpResponse("success")
        response.status_code = 200
        return response

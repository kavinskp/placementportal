from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from Company.models import CompanyInfo
from Company.forms import CompanyInfoForm
from Accounts.models import InterviewerAccount


# Create your views here.

class CompanyInfoDetail(DetailView):
    template_name = 'view_company_info.html'
    context_object_name = 'company'

    def get_object(self, queryset=None):
        interviewer = get_object_or_404(InterviewerAccount, user=self.request.user)
        return interviewer.company_info


def view_company_info(request):
    return render(request, '')


def ajax_load_edit_company_form(request, company_id):
    company_info = CompanyInfo.objects.get(pk=company_id)
    form = CompanyInfoForm(instance=company_info)
    return render(request, 'ajax_load_form_in_card.html', {
        'form': form,
        'form_title': 'Edit Company Information',
    })

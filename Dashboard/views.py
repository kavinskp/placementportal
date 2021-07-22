from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Accounts.models import StaffAccount, StudentAccount, InterviewerAccount, UserType, UserTypeValue


# Create your views here.


def index(request):
    if 'user_name' in request.session:
        return redirect('dashboard')
    return redirect('login')


def company_index(request):
    if 'user_name' in request.session:
        return redirect('dashboard')


@login_required()
def dashboard(request):
    return render(request, 'dashboard.html')

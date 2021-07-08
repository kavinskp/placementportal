from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.clean_password2()
            email = form.clean_email()
            user_obj = authenticate(username=email, password=password)
            login(request, user_obj, 'Accounts.backends.CustomUserAuth')
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    error_message = None
    if request.method == 'POST':
        if 'login' in request.POST:
            request.session.clear()
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_req = authenticate(email=email, password=password)
            if user_req is not None:
                user_obj = CustomUser.objects.get(email=email)
                user_type = user_obj.user_type
                if user_type == 1:
                    if HOD.objects.filter(user=user_obj).exists():
                        hod = HOD.objects.get(user=user_obj)
                        request.session['user_type'] = 'HOD'
                        request.session['is_approved'] = hod.is_approved
                elif user_type == 2:
                    if Staff.objects.filter(user=user_obj).exists():
                        staff = Staff.objects.get(user=user_obj)
                        request.session['user_type'] = 'HOD'
                        request.session['is_approved'] = staff.is_approved
                elif user_type == 3:
                    if Student.objects.filter(user=user_obj).exists():
                        student = Student.objects.get(user=user_obj)
                        request.session['user_type'] = 'HOD'
                        request.session['is_approved'] = student.is_approved
                request.session['curent_user'] = user_obj
                login(request, user_obj, 'Accounts.backends.CustomUserAuth')
                if 'remember_me' in request.POST:
                    request.session['remember_me'] = True
                else:
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/dashboard')
            else:
                error_message = 'Wrong Username or Password'
    return render(request, 'index.html', {'error_message': error_message})


def logout(request):
    return redirect('/')


def profile(request):
    return redirect('/')

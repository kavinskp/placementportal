import hashlib
import random

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import Group

import Accounts.backends
from Accounts.forms import *


# Create your views here.

def signup(request):
    form = SignupForm()
    error = None
    if request.method == 'POST':
        if 'signup' in request.POST:
            form = SignupForm(request.POST)
            if form.is_valid():
                try:
                    password = form.clean_password()
                    email = form.clean_email()
                    random_num_str = str(random.random())
                    hash_val = random_num_str.encode('utf8')
                    hash_val = hashlib.sha1(hash_val).hexdigest()[:5]
                    hash_val = hash_val.encode('utf-8')
                    key = hashlib.sha1(hash_val + email.encode('utf-8'))
                    activation_key = key.hexdigest()
                    acc_type = str(request.POST.get('acc_type'))
                    if acc_type == 'staff':
                        is_staff_acc = True
                    else:
                        is_staff_acc = False

                    key_expires = timezone.now() + timezone.timedelta(days=2)
                    user = CustomUser.objects.create_user(email=email,
                                                          password=password,
                                                          is_staff_account=is_staff_acc,
                                                          activation_key=activation_key,
                                                          key_expires=key_expires,
                                                          )

                    user.is_verified = True
                    user.save()
                    # form.sendEmail({'email': email, 'activation_key': activation_key})

                    msg = {
                        'page_title': 'Placement | Signup success',
                        'title': 'Signup - Success',
                        'description': ["Please Verify Email-ID.",
                                        "An email has been sent your mail ID.",
                                        "Please verify it to proceed"]
                    }
                    return render(request, 'prompt_pages.html', {'message': msg})
                except forms.ValidationError as error_msg:
                    error = error_msg
    return render(request, 'signup.html', {'form': form, 'error': error})


def login_user(request):
    login_form = LoginForm()
    error = None
    request.session.clear()
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                try:
                    email = login_form.clean_email()
                    passwd = login_form.clean_password()
                    user_req = authenticate(email=email, password=passwd)
                    if user_req is not None:
                        user_obj = CustomUser.objects.get(email=email)
                        request.session['user_name'] = user_obj.email
                        request.session['user_id'] = user_obj.pk
                        request.session['is_staff_acc'] = user_obj.is_staff_account
                        if not user_obj.has_filled_profile:
                            return redirect('update_profile_pre_approval')
                        elif user_obj.is_approved:
                            login(request, user_obj, backend='Accounts.backends.CustomUserAuth')
                            if user_obj.is_staff_account:
                                staff_user = Staff.objects.get(user=user_obj)
                                request.session['user_type'] = staff_user.get_designation()
                            else:
                                student = Student.objects.get(user=user_obj)
                                request.session['user_type'] = 'Student'

                            if 'remember_me' in request.POST:
                                request.session['remember_me'] = True
                            else:
                                request.session.set_expiry(0)
                            return redirect('dashboard')
                        else:
                            msg = {
                                'page_title': 'Placement | Login Error',
                                'title': 'Not Approved',
                                'description': ['User is not yet approved!!']
                            }
                            return render(request, 'prompt_pages.html', {'message': msg})
                    else:
                        error = ['Invalid Email Id or Password']
                except forms.ValidationError as error_msg:
                    error = error_msg
                except CustomUser.DoesNotExist:
                    return render_error(request, error_type='user_not_exist')
                except Staff.DoesNotExist:
                    return render_error(request, error_type='user_not_exist', params={'model': 'Staff'})
                except Student.DoesNotExist:
                    return render_error(request, error_type='user_not_exist', params={'model': 'Student'})
    elif request.session and 'remember_me' in request.session:
        return redirect('/dashboard/')
    return render(request, 'login.html', {'form': login_form, 'error': error})


def render_error(request, error_type, params=None):
    if error_type == 'user_not_exist':
        user = 'User'
        if params is not None:
            if 'model' in params:
                user = params.get('model')
        desc = [user + ' Doesnt Exist!']
        msg = {
            'page_title': 'Placement | Login Error',
            'title': 'Invalid account',
            'description': desc
        }
        return render(request, 'prompt_pages.html', {'message': msg})
    msg = {
        'page_title': 'Placement | Error',
        'title': 'Unknown Error',
        'description': ['Unknown Error Occurred!']
    }
    return render(request, 'prompt_pages.html', {'message': msg})


def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')


def profile(request):
    return redirect('/')


def update_profile_pre_approval(request):
    form = None
    error = None
    if request.method == 'POST':
        acc_type = request.POST['acc_type']
        user_name = request.POST['user_name']
        if 'student' in request.POST:
            form = UpdateProfileStudent(request.POST)
            if form.is_valid():
                try:
                    student_obj = form.save(commit=False)
                    user_obj = CustomUser.objects.get(email=user_name)
                    print(user_obj)
                    g = Group.objects.get(name='Student')
                    g.user_set.add(user_obj)
                    print(g.user_set.last())
                    student_obj.user = user_obj
                    student_obj.save()
                    user_obj.has_filled_profile = True
                    user_obj.save()

                    msg = {
                        'page_title': 'Placement | Update Success',
                        'title': 'Profile updated SuccessFully',
                        'description': ['Once account approved !! You can login!!']
                    }
                    return render(request, 'prompt_pages.html', {'message': msg})
                except Exception as e:
                    error = [str(e)]
            else:
                error = ['Update Failed!!']
        elif 'staff' in request.POST:
            form = UpdateProfileStaff(request.POST)
            if form.is_valid():
                try:
                    staff_obj = form.save(commit=False)
                    user_obj = CustomUser.objects.get(email=user_name)
                    designation = request.POST['designation']
                    print(designation)
                    if designation == '2':
                        group = Group.objects.get(name='HOD')
                        group.user_set.add(user_obj)
                        print(len(group.user_set.all()))
                    else:
                        group = Group.objects.get(name='Faculty')
                        group.user_set.add(user_obj)
                        print(len(group.user_set.all()))
                    print(len(group.user_set.all()))
                    staff_obj.user = user_obj
                    staff_obj.save()
                    user_obj.has_filled_profile = True
                    user_obj.save()
                    msg = {
                        'page_title': 'Placement | Update Success',
                        'title': 'Profile updated SuccessFully',
                        'description': ['Once account approved !! You can login!!']
                    }
                    return render(request, 'prompt_pages.html', {'message': msg})
                except Exception as e:
                    error = [str(e)]
            else:
                error = ['Update Failed!!']
    elif request.session is not None:
        if 'user_name' in request.session:
            user_name = request.session.get('user_name')
            if 'is_staff_acc' in request.session:
                is_staff_acc = bool(request.session.get('is_staff_acc'))
                if is_staff_acc:
                    form = UpdateProfileStaff()
                    acc_type = 'staff'
                else:
                    form = UpdateProfileStudent()
                    acc_type = 'student'
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        return redirect('login')
    return render(request, 'update_profile.html',
                  {'form': form, 'acc_type': acc_type, 'user_name': user_name, 'error': error})

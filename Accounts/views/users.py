import hashlib
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from Accounts.forms import *
from Accounts.models import UserType, StaffAccount, StudentAccount, InterviewerAccount

# Create your views here.
INTERVIEWER = 'Interviewer'
STAFF = 'Staff'
STUDENT = 'Student'


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
                    user_type = request.POST.get('user_type')

                    key_expires = timezone.now() + timezone.timedelta(days=2)
                    user = CustomUser.objects.create_user(email=email,
                                                          password=password,
                                                          user_type=user_type,
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
                    error = [error_msg]
    return render(request, 'signup.html', {'form': form, 'error_msg': error})


def login_user(request):
    login_form = LoginForm()
    error = None
    request.session.clear()
    invalid_cred = False
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                try:
                    email = login_form.clean_email()
                    passwd = login_form.clean_password()
                    user_req = authenticate(request, username=email, password=passwd)
                    if user_req is not None:
                        user_obj = CustomUser.objects.get(email=email)
                        request.session['user_name'] = user_obj.email
                        if not user_obj.has_filled_profile:
                            return redirect('update_profile_pre_approval')
                        elif not user_obj.account_created:
                            return redirect('update_profile_pre_approval')
                        elif user_obj.is_approved:
                            if user_obj.is_active:
                                login(request, user_obj, backend='Accounts.backends.CustomUserAuth')
                                if 'remember_me' in request.POST:
                                    request.session['remember_me'] = True
                                else:
                                    request.session.set_expiry(0)
                                return redirect('dashboard')
                            else:
                                msg = {
                                    'page_title': 'Placement | Login Error',
                                    'title': 'Not Active',
                                    'description': ['User is not active!!']
                                }
                        else:
                            msg = {
                                'page_title': 'Placement | Login Error',
                                'title': 'Not Approved',
                                'description': ['User is not yet approved!!']
                            }
                        return render(request, 'prompt_pages.html', {'message': msg})
                    else:
                        invalid_cred = True
                except forms.ValidationError as error_msg:
                    error = error_msg
                except CustomUser.DoesNotExist:
                    invalid_cred = True
                except StaffAccount.DoesNotExist:
                    invalid_cred = True
                except StudentAccount.DoesNotExist:
                    invalid_cred = True
                except InterviewerAccount.DoesNotExist:
                    invalid_cred = True
            else:
                invalid_cred = True
    elif request.session and 'remember_me' in request.session:
        return redirect('dashboard')
    if invalid_cred:
        error = ['Invalid Username or Password']
    return render(request, 'login.html', {'form': login_form, 'error_msg': error})


def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')


def update_profile_pre_approval(request):
    form = None
    error = None
    form_name = None
    user_name = None
    if request.method == 'POST':
        form_name = request.POST['form_name']
        user_name = request.POST['user_name']
        if form_name is None:
            return redirect('login')
        elif form_name == 'UserProfileForm':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    profile_obj = form.save()
                    user_obj = CustomUser.objects.get(email=user_name)
                    user_obj.profile = profile_obj
                    user_obj.has_filled_profile = True
                    if user_obj.user_type == UserType.INTERVIEWER.value:
                        user_obj.account_created = True
                    user_obj.save()
                    return redirect('update_profile_pre_approval')
                except Exception as e:
                    error = [str(e)]
            else:
                error = ['Update Failed!!']
        elif form_name == 'StaffAccountForm':
            form = StaffAccountForm(request.POST)
            if form.is_valid():
                try:
                    staff_obj = form.save(commit=False)
                    user_obj = CustomUser.objects.get(email=user_name)
                    if user_obj.user_type == UserType.ADMIN.value:
                        admin_group = Group.objects.get(name='Principal')
                        admin_group.user_set.add(user_obj)
                        staff_obj.designation = 1
                    group = Group.objects.get(name='Faculty')
                    group.user_set.add(user_obj)
                    staff_obj.user = user_obj
                    staff_obj.save()
                    user_obj.account_created = True
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
        elif form_name == 'StudentInfoForm':
            form = StudentInfoForm(request.POST)
            if form.is_valid():
                try:
                    student_info = form.save()
                    user_obj = CustomUser.objects.get(email=user_name)
                    if StudentAccount.objects.filter(user=user_obj):
                        raise forms.ValidationError('Account Already Exists')
                    else:
                        StudentAccount.objects.create(
                            user=user_obj,
                            info=student_info
                        )
                    user_obj.account_created = True
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

        else:
            return redirect('login')
    elif request.session is not None:
        if 'user_name' in request.session:
            user_name = request.session.get('user_name')
            user_obj = CustomUser.objects.get(email=user_name)
            if user_obj is None:
                return redirect('login')
            else:
                if user_obj.has_filled_profile:
                    user_type = user_obj.user_type
                    if user_type is not None:
                        if user_type == UserType.ADMIN.value:
                            form_name = 'StaffAccountForm'
                            form = StaffAccountForm()
                        elif user_type == UserType.STAFF.value:
                            form_name = 'StaffAccountForm'
                            form = StaffAccountForm()
                        elif user_type == UserType.STUDENT.value:
                            form_name = 'StudentInfoForm'
                            form = StudentInfoForm()
                        elif user_type == UserType.INTERVIEWER.value:
                            return redirect('login')
                else:
                    form_name = 'UserProfileForm'
                    form = UserProfileForm()
        else:
            return redirect('login')
    else:
        return redirect('login')
    return render(request, 'update_profile.html',
                  {'form': form, 'form_name': form_name, 'user_name': user_name,
                   'error_msg': error})

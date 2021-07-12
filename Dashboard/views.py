from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Accounts.models import Staff, Student


# Create your views here.


def index(request):
    if 'user_name' in request.session:
        return redirect('dashboard')
    return redirect('login')


@login_required()
def dashboard(request):
    if request.session is not None:
        is_staff_acc = bool(request.session.get('is_staff_acc'))
        if is_staff_acc:
            user_obj = Staff.objects.get(user=request.user)
        else:
            user_obj = Student.objects.get(user=request.user)
        return render(request, 'dashboard.html', {
            'user_obj': user_obj,
        })
    return redirect('login')

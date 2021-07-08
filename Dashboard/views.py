from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    if request.session and 'remember_me' in request.session:
        return redirect('/dashboard')
    return redirect('login')


def dashboard(request):
    return render(request, 'dashboard.html')

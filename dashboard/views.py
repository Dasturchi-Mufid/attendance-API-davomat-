from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import models

@login_required(login_url='login')
def index(request):
    employers = []
    queryset = models.Employee.objects.all()
    for i in queryset:
        if models.Attendance.objects.filter(employee__name=i.name,come_out__isnull=True):
            i.come = True
        else:
            i.come = False
        employers.append(i)
    context = {
        'employers': employers,
    }
    return render(request, 'dashboard/index.html', context)



def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request,'auth/login.html')
        except:
            return redirect('login')
    return render(request, 'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('login')
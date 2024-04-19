from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .funcs import staff_required
from . import models

@staff_required
def index(request):
    employers = []
    queryset = models.Employee.objects.filter(date_of_leaving__isnull=True)
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

@staff_required
def create_employee(request):

    choices = models.Employee.status.field.choices

    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')
        avatar = request.FILES.get('avatar')
        print(name, status, avatar)
        models.Employee.objects.create(
            name=name,
            status=status,
            avatar=avatar,
        )
        return redirect('list_employee')

    context = {'choices': choices}
    return render(request,'employee/create.html', context)

@staff_required
def list_employee(request):
    employers = models.Employee.objects.all()
    choices = models.Employee.status.field.choices
    context = { 
        'employers': employers,
        'choices': choices,
        }
    return render(request,'employee/list.html',context)


@staff_required
def edit_employee(request, code):
    
    choices = models.Employee.status.field.choices
    employer = models.Employee.objects.get(code=code)

    if request.method == 'POST':
        employer.name = request.POST.get('name')
        employer.status = request.POST.get('status')
        if request.FILES:
            employer.avatar = request.FILES.get('avatar')
        employer.save()
        return redirect('list_employee')
    
    context = {
        'employer':employer,
        'choices': choices,
        }
    return render(request,'employee/edit.html',context)


def delete_employee(request, code):
    employer = models.Employee.objects.get(code=code)
    employer.delete()
    return redirect('list_employee')

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
    redirect('logout')
    return render(request, 'auth/logout.html')
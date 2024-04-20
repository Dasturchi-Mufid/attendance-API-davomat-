from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage

from datetime import datetime


from .funcs import staff_required
from . import models


def paginator_page(List,num,request):
    paginator = Paginator(List,num)
    page = request.GET.get('page')
    try:
        List = paginator.page(page)
    except PageNotAnInteger:
        List = paginator.page(1)
    except EmptyPage:
        List = paginator.page(paginator.num_pages)
    return List

@staff_required
def index(request):
    employers = []
    queryset = models.Employee.objects.filter(date_of_leaving__isnull=True)
    for i in queryset:
        if models.Attendance.objects.filter(employee__name=i.name,come_in__day=datetime.now().day):
            i.come = True
        elif models.Attendance.objects.filter(employee__name=i.name,come_out__day=datetime.now().day):
            i.come = False
        else:
            continue
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
        'employers': paginator_page(employers,10,request),
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


@staff_required
def history_employee(request,code):
    employer = models.Employee.objects.get(code=code)
    attendance = models.Attendance.objects.filter(employee=employer)[::-1]
    context = {'attendance':paginator_page(attendance,10,request)}
    return render(request,'employee/history.html',context)

@staff_required
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

@staff_required
def profile(request):
    employers = models.Employee.objects.all().count()
    users = User.objects.all().count()
    context = {
        'employers': employers,
        'users': users,
    }
    return render(request, 'auth/profile.html', context=context)


@staff_required
def edit_profile(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('profile')

def attendance_list(request):
    employers = models.Attendance.objects.filter(employee__date_of_leaving__isnull=True)[::-1]
    if request.GET.get('come'):
        filter_items = {}
        for key, value in request.GET.items():
            if value:
                if key == 'start_date':
                    values = value.split('-')
                    year, month, day = int(values[0]),int(values[1]),int(values[2])
                    key = 'come_in__gte'
                    value = datetime(year=year,month=month,day=day)
                elif key == 'end_date':    
                    values = value.split('-')
                    year, month, day = int(values[0]),int(values[1]),int(values[2])
                    key = 'come_in__lte'
                    value = datetime(year=year,month=month,day=day)
                elif key == 'name':
                    key = 'employee__name__icontains'
                elif key == 'come' and value == 'come_in':
                    key = 'come_out__isnull'
                    value = True
                elif key == 'come' and value == 'come_out':
                    key = 'come_out__isnull'
                    value = False
                elif key == 'come' and value == 'all':
                    continue
                filter_items[key] = value
        employers = models.Attendance.objects.filter(**filter_items)
        print(filter_items)
    context = {'employers': employers}
    return render(request, 'attendance/list.html',context)


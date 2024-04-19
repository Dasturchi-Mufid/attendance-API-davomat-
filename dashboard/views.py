from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models

# @login_required(login_url='login')
def index(request):
    employers = models.Employee.objects.all()
    context = {
        'employers': employers,
    }
    return render(request, 'dashboard/index.html', context)

def login(request):
    return render(request, 'dashboard/login.html')
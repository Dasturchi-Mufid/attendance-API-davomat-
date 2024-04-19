from . import models

def employees(request):
    employees = models.Employee.objects.all()
    return {'employees': employees}
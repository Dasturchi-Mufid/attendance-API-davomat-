from django.db import models
from django.core.files.storage import default_storage
from datetime import datetime

class Employee(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=(
            ('OTH', 'Other'),
            ('MGR', 'Manager'),
            ('EMP', 'Employee'),
            ('INT', 'Intern'),
            ('ADM', 'Administrator'),
            )
        )
    avatar = models.ImageField(upload_to='avatars/')
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def delete(self):
        avatar_path = self.avatar.path
        if default_storage.exists(avatar_path):
            default_storage.delete(avatar_path)
        super(Employee, self).delete()

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    come_in = models.DateTimeField(null=True, blank=True)
    come_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} {str(self.time_in)} - {str(self.time_out)}"
    
    def save(self,*args, **kwargs):
        if self.pk:
            self.come_out = datetime.now()
        else:
            self.come_in = datetime.now()
        super(Attendance, self).save(*args, **kwargs)



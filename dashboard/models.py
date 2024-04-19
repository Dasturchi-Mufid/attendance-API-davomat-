from django.db import models
from django.core.files.storage import default_storage
from datetime import datetime

class Employee(models.Model):
    """
    Model representing an employee.

    Attributes:
        name (str): The name of the employee.
        status (str): The status of the employee. Choices are 'Other', 'Manager', 'Employee', 'Intern', 'Administrator'.
        avatar (File): The avatar image of the employee.
        date_of_joining (Date): The date the employee joined the company.
        date_of_leaving (Date, optional): The date the employee left the company, if applicable.
    """

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
        """
        Returns a string representation of the employee.
        """
        return self.name
    
    def delete(self):
        """
        Deletes the employee and their associated avatar from the storage.
        """
        avatar_path = self.avatar.path
        if default_storage.exists(avatar_path):
            default_storage.delete(avatar_path)
        super(Employee, self).delete()

class Attendance(models.Model):
    """
    Model representing employee attendance.

    Attributes:
        employee (Employee): The employee associated with the attendance record.
        come_in (DateTime, optional): The date and time the employee came in.
        come_out (DateTime, optional): The date and time the employee went out.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    come_in = models.DateTimeField(blank=True)
    come_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the attendance record.
        """
        return f"{self.employee.name} {str(self.come_in)} - {str(self.come_out)}"

    
    def save(self, *args, **kwargs):
        """
        Saves the attendance record and updates come_in and come_out fields based on whether it's a new record or an update.
        """
        if not self.pk:
            obj = Attendance.objects.filter(employee=self.employee, come_out__isnull=True).first()
            if obj:
                obj.come_out = datetime.now()
                obj.save()
                return
            else:
                self.come_in = datetime.now()
        super(Attendance, self).save(*args, **kwargs)
from dashboard import models
from rest_framework.serializers import ModelSerializer

class EmployeeListSerializer(ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class AttendanceListSerializer(ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = '__all__'
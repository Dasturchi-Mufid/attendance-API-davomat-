from django.urls import path
from . import views

urlpatterns = [
    path('staff-list/',views.staff_list),
    path('attendance-create/',views.attendance_create),
]

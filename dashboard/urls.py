from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('attendance/',views.attendance_list,name='attendance_list'),
    path('employee/create',views.create_employee,name='create_employee'),
    path('employee/list',views.list_employee,name='list_employee'),
    path('employee/edit/<str:code>/',views.edit_employee,name='edit_employee'),
    path('employee/delete/<str:code>/',views.delete_employee,name='delete_employee'),
    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('edit-profile/<int:id>/',views.edit_profile,name='edit_profile'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('open-elective/<int:elective>/application', views.open_elective_application, name='open_elective_application'),
    path('department-elective/<int:elective>/application', views.department_elective_application, name='department_elective_application'),
]
from django.urls import path
from .views import (
    OpenElectiveSubjectDetailView,
    DepartmentElectiveSubjectDetailView
)
from . import views

urlpatterns = [
    path('open-elective-subject/<int:pk>', OpenElectiveSubjectDetailView.as_view(), name='open_elective_subject'),
    path('department-elective-subject/<int:pk>', DepartmentElectiveSubjectDetailView.as_view(), name='department_elective_subject'),
]
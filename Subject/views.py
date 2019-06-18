from django.shortcuts import render
from .models import OpenElectiveSubject, DepartmentElectiveSubject
from django.views.generic import DetailView


class OpenElectiveSubjectDetailView(DetailView):
    model = OpenElectiveSubject
    template_name = 'Subject/open-elective-subject.html'


class DepartmentElectiveSubjectDetailView(DetailView):
    model = DepartmentElectiveSubject
    template_name = 'Subject/department-elective-subject.html'
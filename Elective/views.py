from django.shortcuts import render, redirect
from .models import OpenElective, DepartmentElective
from django.views.generic import ListView

def index(request):
    return redirect('open_elective')

def guidelines(request):
    return render(request, 'Elective/guidelines.html')


class OpenElectiveListView(ListView):
    model = OpenElective
    template_name = 'Elective/open-elective.html'
    context_object_name = 'electives'
    ordering = ['-ends']


class DepartmentElectiveListView(ListView):
    model = DepartmentElective
    template_name = 'Elective/department-elective.html'
    context_object_name = 'electives'
    ordering = ['-ends']
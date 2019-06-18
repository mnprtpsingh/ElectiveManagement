from django.urls import path
from .views import (
    OpenElectiveListView,
    DepartmentElectiveListView
)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('open-elective/', OpenElectiveListView.as_view(), name='open_elective'),
    path('department-elective/', DepartmentElectiveListView.as_view(), name='department_elective'),
    path('guidelines/', views.guidelines, name='guidelines'),
]
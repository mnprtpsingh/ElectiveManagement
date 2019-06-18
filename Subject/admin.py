from django.contrib import admin
from .models import OpenElectiveSubject, DepartmentElectiveSubject


class ElectiveSubjectAdmin(admin.ModelAdmin):
    search_fields = ('-elective', 'course_code')
    ordering = ('-elective', 'course_code')


@admin.register(OpenElectiveSubject)
class OpenElectiveSubjectAdmin(ElectiveSubjectAdmin):
    def has_change_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.department

    def has_delete_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.department


@admin.register(DepartmentElectiveSubject)
class DepartmentElectiveSubjectAdmin(ElectiveSubjectAdmin):
    def has_change_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.elective.department

    def has_delete_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.elective.department

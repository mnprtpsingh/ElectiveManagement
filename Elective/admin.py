from django.contrib import admin
from .models import OpenElective, DepartmentElective


class ElectiveAdmin(admin.ModelAdmin):
    filter_horizontal = ('batches',)
    ordering = ('-ends',)


@admin.register(OpenElective)
class OpenElectiveAdmin(ElectiveAdmin):
    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.is_admin

    def has_change_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin

    def has_delete_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin


@admin.register(DepartmentElective)
class DepartmentElectiveAdmin(ElectiveAdmin):
    def has_change_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.department

    def has_delete_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.department

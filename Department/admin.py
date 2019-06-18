from django.contrib import admin
from .models import Department, Batch


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.is_admin or request.user.staff.department == object

    def has_delete_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.is_admin or request.user.staff.department == object


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    ordering = ('-year',)

    def has_change_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin

    def has_delete_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin

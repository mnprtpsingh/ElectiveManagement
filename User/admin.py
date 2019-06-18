from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Staff, Student


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit: user.save()
        return user


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('name', 'email')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('name', 'email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ()
    ordering = ('name',)
    filter_horizontal = ()

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.is_admin

    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.is_admin

    def has_view_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin

    def has_change_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin

    def has_delete_permission(self, request, object=None):
        return request.user.is_authenticated and request.user.is_admin


class StaffCreationForm(UserCreationForm):

    class Meta:
        model = Staff
        fields = ('name', 'email', 'department')


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    add_form = StaffCreationForm

    list_display = ('name', 'email', 'department')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'department')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'department', 'password1', 'password2')}
        ),
    )
    ordering = ('department', 'name',)


# class StudentForm(forms.ModelForm):
#     def clean_roll_number(self):
#         roll_number = self.cleaned_data.get("roll_number")
#         return roll_number.upper()


# class StudentCreationForm(StudentForm):

#     class Meta:
#         model = Student
#         fields = ('roll_number', 'name', 'email', 'department', 'batch')


# class StudentChangeForm(StudentForm):

#     class Meta:
#         model = Student
#         fields = ('roll_number', 'name', 'email', 'department', 'batch', 'password')

#     def save(self, commit=True):
#         student = super().save(commit=False)
#         password = self.cleaned_data.get("password")
#         if password and not student.check_password(password):
#             raise forms.ValidationError("Invalid Password")
#         if commit: student.save()
#         return student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'department', 'batch')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('roll_number', 'name', 'email', 'department', 'batch')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('roll_number', 'name', 'email', 'department', 'batch')}
        ),
    )
    search_fields = ('roll_number',)
    ordering = ('-batch', 'roll_number')
    filter_horizontal = ()

    def has_change_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.department

    def has_delete_permission(self, request, object=None):
        if not (request.user.is_authenticated and request.user.is_staff): return False
        if not object: return request.user.is_staff
        return request.user.staff and request.user.staff.department == object.department


# admin.site.register(Administrator)
admin.site.unregister(Group)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Elective.models import OpenElective, DepartmentElective
from .models import (
    DepartmentElectiveSubjectPreference,
    OpenElectiveSubjectPreference,
    DepartmentElectiveApplication,
    OpenElectiveApplication,
)
from User.models import Student
from django.db import transaction
from datetime import date
from random import shuffle


@login_required
def open_elective_application(request, elective):
    user = request.user
    student = get_object_or_404(Student, user=user)
    elective = get_object_or_404(OpenElective, id=elective)
    if student.batch not in elective.batches.all():
        return redirect('open_elective')
    application, created = OpenElectiveApplication.objects.get_or_create(student=student, elective=elective)
    if request.method == "GET":
        subjects = application.applicable_subjects
        if len(application.preferences.all()) != len(subjects): # TODO
            preference_numbers = list(range(1, len(subjects)+1))
            shuffle(preference_numbers)
            with transaction.atomic():
                for index, subject in enumerate(subjects):
                    application.subject_preferences.create(
                        preference_number=preference_numbers[index],
                        subject=subject
                    )
    elif request.method == "POST":
        if elective.starts > date.today() or elective.ends < date.today():
            return redirect('open_elective')
        cgpa = request.POST.get('cgpa')
        try:
            cgpa = float(cgpa)
            if cgpa < 0 or cgpa > 10:
                raise ValueError
            application.cgpa = cgpa
        except ValueError:
            return redirect(request.path)
        preferences = list(map(int, request.POST.get('preferences').split()))
        subjects = application.applicable_subjects
        if len(preferences) != len(subjects):
            return redirect(request.path)
        try:
            with transaction.atomic():
                application.save()
                for index, preference in enumerate(preferences):
                    subject_preference = application.subject_preferences.get(subject=preference)
                    subject_preference.preference_number = index + 1
                    subject_preference.save()
        except OpenElectiveSubjectPreference.DoesNotExist:
            return redirect(request.path)
        available_subjects = list(elective.elective_subjects.all())
        application.allocate_subjects(available_subjects)
    return render(request, 'Application/open-elective-application.html', {'application': application})


@login_required
def department_elective_application(request, elective):
    user = request.user
    student = get_object_or_404(Student, user=user)
    elective = get_object_or_404(DepartmentElective, id=elective)
    department = elective.department
    if student.batch not in elective.batches.all() or student.department != department:
        return redirect('department_elective')
    application, created = DepartmentElectiveApplication.objects.get_or_create(student=student, elective=elective)
    if request.method == "GET":
        if len(application.preferences.all()) == 0:
            subjects = application.applicable_subjects
            preference_numbers = list(range(1, len(subjects)+1))
            shuffle(preference_numbers)
            with transaction.atomic():
                for index, subject in enumerate(subjects):
                    application.subject_preferences.create(
                        preference_number=preference_numbers[index],
                        subject=subject
                    )
    elif request.method == "POST":
        if elective.starts > date.today() or elective.ends < date.today():
            return redirect('department_elective')
        cgpa = request.POST.get('cgpa')
        try:
            cgpa = float(cgpa)
            if cgpa < 0 or cgpa > 10:
                raise ValueError
            application.cgpa = cgpa
        except ValueError:
            return redirect(request.path)
        preferences = list(map(int, request.POST.get('preferences').split()))
        subjects = application.applicable_subjects
        if len(preferences) != len(subjects):
            return redirect(request.path)
        try:
            with transaction.atomic():
                application.save()
                for index, preference in enumerate(preferences):
                    subject_preference = application.subject_preferences.get(subject=preference)
                    subject_preference.preference_number = index + 1
                    subject_preference.save()
        except DepartmentElectiveSubjectPreference.DoesNotExist:
            return redirect(request.path)
        available_subjects = list(elective.elective_subjects.all())
        application.allocate_subjects(available_subjects)
    return render(request, 'Application/department-elective-application.html', {'application': application})

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from .models import (
    OpenElectiveSubject,
    DepartmentElectiveSubject
)
from random import shuffle


def allocate_subject(application, student_strength):
    number_of_courses = application.elective.number_of_courses
    applicable_subjects = application.applicable_subjects
    preference_numbers = list(range(1, len(applicable_subjects)+1))
    shuffle(preference_numbers)
    allotted_subjects = []
    with transaction.atomic():
        for index, subject in enumerate(applicable_subjects):
            preference = application.subject_preferences.filter(subject=subject).first()
            if not preference:
                application.subject_preferences.create(
                    preference_number=preference_numbers[index],
                    subject=subject
                )
            else:
                preference.preference_number = preference_numbers[index]
                preference.save()
        for preference in application.subject_preferences.all():
            subject = preference.subject
            if student_strength[subject] < subject.maximum_seats:
                allotted_subjects.append(subject)
                student_strength[subject] += 1
            if len(allotted_subjects) == number_of_courses:
                application.allotted_subjects.set(allotted_subjects)
                break

@receiver(post_save, sender=OpenElectiveSubject)
def allocate_open_elective_subject(sender, instance, created, **kwargs):
    if not created: return
    elective = instance.elective
    subjects = elective.elective_subjects.all()
    student_strength = {}
    for subject in subjects:
        student_strength[subject] = 0
    for batch in elective.batches.all():
        for student in batch.students.all():
            application, created = student.open_elective_applications.get_or_create(elective=elective)
            allocate_subject(application, student_strength)

@receiver(post_save, sender=DepartmentElectiveSubject)
def allocate_department_elective_subject(sender, instance, created, **kwargs):
    if not created: return
    elective = instance.elective
    department = elective.department
    subjects = elective.elective_subjects.all()
    student_strength = {}
    for subject in subjects:
        student_strength[subject] = 0
    for batch in elective.batches.all():
        for student in batch.students.all():
            if student.department is not department: return
            application, created = student.department_elective_applications.get_or_create(elective=elective)
            allocate_subject(application, student_strength)

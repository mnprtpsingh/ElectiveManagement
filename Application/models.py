from django.db import models, transaction
from django.urls import reverse
from User.models import Student
from Elective.models import (
    OpenElective,
    DepartmentElective
)
from Subject.models import (
    OpenElectiveSubject,
    DepartmentElectiveSubject
)


class ElectiveApplication(models.Model):
    cgpa = models.FloatField(verbose_name='CGPA', default=0.0)
    verified = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def allocate_subjects(self, available_subjects):
        number_of_courses = self.elective.number_of_courses
        preferences = self.subject_preferences.filter(subject__in=available_subjects)
        allotted_subjects = list(self.allotted_subjects.all())
        if len(allotted_subjects) != 0:
            for preference in preferences:
                if preference.subject in allotted_subjects:
                    number = preference.preference_number
            preferences = preferences.filter(preference_number__gt=number)
        with transaction.atomic():
            for preference in preferences:
                subject = preference.subject
                application = subject.enroll_applicant(self)
                if application is None: allotted_subjects.append(subject)
                elif application is not self:
                    available_subjects.remove(subject)
                    application.allocate_subjects(available_subjects)
                if len(allotted_subjects) == number_of_courses:
                    self.allotted_subjects.set(allotted_subjects)
                    break


class OpenElectiveApplication(ElectiveApplication):
    student = models.ForeignKey(Student, related_name='open_elective_applications', on_delete=models.CASCADE)
    elective = models.ForeignKey(OpenElective, related_name='applications', on_delete=models.CASCADE)
    preferences = models.ManyToManyField(
        OpenElectiveSubject,
        through='OpenElectiveSubjectPreference',
        through_fields=('application', 'subject'),
        related_name='applications'
    )
    allotted_subjects = models.ManyToManyField(
        OpenElectiveSubject,
        related_name='enrolled_students'
    )

    class Meta:
        unique_together = [['student', 'elective']]
        ordering = ['elective', '-cgpa']

    @property
    def applicable_subjects(self):
        subjects = OpenElectiveSubject.objects.filter(elective=self.elective)
        subjects = subjects.exclude(department=self.student.department)
        return subjects.exclude(subject__in=self.student.subjects.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cgpa = round(self.cgpa, 2)


class DepartmentElectiveApplication(ElectiveApplication):
    student = models.ForeignKey(Student, related_name='department_elective_applications', on_delete=models.CASCADE)
    elective = models.ForeignKey(DepartmentElective, related_name='applications', on_delete=models.CASCADE)
    preferences = models.ManyToManyField(
        DepartmentElectiveSubject,
        through='DepartmentElectiveSubjectPreference',
        through_fields=('application', 'subject'),
        related_name='applications'
    )
    allotted_subjects = models.ManyToManyField(
        DepartmentElectiveSubject,
        related_name='enrolled_students'
    )

    class Meta:
        unique_together = [['student', 'elective']]
        ordering = ['elective', '-cgpa']

    @property
    def applicable_subjects(self):
        subjects = DepartmentElectiveSubject.objects.filter(elective=self.elective)
        return subjects.exclude(subject__in=self.student.subjects.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cgpa = round(self.cgpa, 2)


class ElectiveSubjectPreference(models.Model):
    preference_number = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


class OpenElectiveSubjectPreference(ElectiveSubjectPreference):
    application = models.ForeignKey(OpenElectiveApplication, related_name='subject_preferences', on_delete=models.CASCADE)
    subject = models.ForeignKey(OpenElectiveSubject, related_name='preferences', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['application', 'subject', 'preference_number']]
        ordering = ['application', 'preference_number']


class DepartmentElectiveSubjectPreference(ElectiveSubjectPreference):
    application = models.ForeignKey(DepartmentElectiveApplication, related_name='subject_preferences', on_delete=models.CASCADE)
    subject = models.ForeignKey(DepartmentElectiveSubject, related_name='preferences', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['application', 'subject', 'preference_number']]
        ordering = ['application', 'preference_number']

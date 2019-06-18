from django.db import models
from django.urls import reverse
from Department.models import Department
from Elective.models import OpenElective, DepartmentElective
from datetime import date
from random import shuffle


class Subject(models.Model):
    subject_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.subject_name

    def get_absolute_url(self):
        return reverse('subject', kwargs={'pk': self.pk})


class ElectiveSubject(models.Model):
    course_code = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    subject_teacher = models.CharField(max_length=50, blank=True)
    minimum_seats = models.IntegerField()
    maximum_seats = models.IntegerField()
    # elective = models.ForeignKey(Elective, on_delete=models.CASCADE)
    syllabus_link = models.URLField(blank=True, help_text='Can be a URL to google drive...')

    class Meta:
        abstract = True

    def __str__(self):
        return self.course_code + ": " + str(self.subject)

    def enroll_applicant(self, application):
        enrolled_students = self.enrolled_students.all()
        if enrolled_students.count() < self.maximum_seats:
            return self.enrolled_students.add(application)
        last_applicant = enrolled_students.last()
        if last_applicant.cgpa < application.cgpa:
            self.enrolled_students.remove(last_applicant)
            self.enrolled_students.add(application)
            return last_applicant
        else: return application


class OpenElectiveSubject(ElectiveSubject):
    elective = models.ForeignKey(OpenElective, related_name='elective_subjects', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='+', on_delete=models.CASCADE, help_text='Offered by...')

    class Meta:
        verbose_name = 'Open Elective Subject'
        verbose_name_plural = 'Open Elective Subjects'

    # @property
    # def cutoff(self):
    #     if self.enrolled_students.count() < self.maximum_seats: return 0
    #     return self.enrolled_students.aggregate(Min('cgpa'))['cgpa__min']

    def save(self, *args, **kwargs):
        if self.id is None and self.elective.starts <= date.today(): return
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.elective.ends < date.today(): return
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('open_elective_subject', kwargs={'pk': self.pk})


class DepartmentElectiveSubject(ElectiveSubject):
    elective = models.ForeignKey(DepartmentElective, related_name='elective_subjects', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Department Elective Subject'
        verbose_name_plural = 'Department Elective Subjects'

    # @property
    # def cutoff(self):
    #     if self.enrolled_students.count() < self.maximum_seats: return 0
    #     return self.enrolled_students.aggregate(Min('cgpa'))['cgpa__min']

    def save(self, *args, **kwargs):
        if self.elective.starts <= date.today(): return
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.elective.ends < date.today(): return
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('department_elective_subject', kwargs={'pk': self.pk})
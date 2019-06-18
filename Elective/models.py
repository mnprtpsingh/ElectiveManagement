from django.db import models, transaction
from Department.models import Department, Batch


class Elective(models.Model):
    batches = models.ManyToManyField(
        Batch,
        related_name='+',
        help_text="The batch of 3rd year students should be 2 or 3 years past the current year, " +
            "for final year students it will be 3 or 4 years past the current year... " +
            "also you have to add dual degree batches explicitly as it is not same as b. tech."
    )
    number_of_courses = models.IntegerField(
        help_text="Number of courses that will be alloted to each student"
    )
    starts = models.DateField(
        help_text="Once students start filling preferences, subjects offered can't be removed"
    )
    ends = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.starts.strftime("%d %B, %Y") + " - " + self.ends.strftime("%d %B, %Y")


class OpenElective(Elective):
    # elective = models.OneToOneField(Elective, on_delete=models.CASCADE, parent_link=True)

    class Meta:
        verbose_name = 'Open Elective'
        verbose_name_plural = 'Open Electives'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for batch in self.batches.all():
            for student in batch.students.all():
                student.open_elective_applications.create(elective=self)


class DepartmentElective(Elective):
    # elective = models.OneToOneField(Elective, on_delete=models.CASCADE, parent_link=True)
    department = models.ForeignKey(Department, related_name='+', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Department Elective'
        verbose_name_plural = 'Department Electives'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for batch in self.batches.all():
            for student in batch.students.all():
                if student.department is self.department:
                    student.department_elective_applications.create(elective=self)
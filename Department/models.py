from django.db import models, transaction
from django.urls import reverse
from datetime import date


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department', kwargs={'pk': self.pk})


class Degree(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Batch(models.Model):
    degree = models.ForeignKey(Degree, related_name='+', on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField(help_text='Year of Joining Institute')

    class Meta:
        verbose_name_plural = 'Batches'

    @transaction.atomic
    def save(self, *args, **kwargs):
        Batch.objects.filter(year__lt=date.today().year - 5).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.degree) + " - " + str(self.year)

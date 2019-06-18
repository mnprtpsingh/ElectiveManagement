from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db import models

from Department.models import Department, Batch
from Subject.models import Subject


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(
            name=name,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(
            name=name,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        # abstract = True
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


# class Administrator(User):

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.is_admin = True


class Staff(User):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, parent_link=True)
    department = models.ForeignKey(Department, related_name='+', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Staff'

    @property
    def is_staff(self):
        return True


class Student(User):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, parent_link=True)
    roll_number = models.CharField(max_length=15, unique=True)
    batch = models.ForeignKey(Batch, related_name='students', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='+', on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='+')

    def __str__(self):
        return self.roll_number

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.roll_number = self.roll_number.upper()
from django.contrib.auth.backends import ModelBackend
from backend.models import Administrator, Staff, Student


class UserBackend(ModelBackend):

    def authenticate(self, *args, **kwargs):
        return self.downcast_user_type(super().authenticate(*args, **kwargs))

    def get_user(self, *args, **kwargs):
        return self.downcast_user_type(super().get_user(*args, **kwargs))

    def downcast_user_type(self, user):
        try:
            student = Student.objects.get(pk=user.pk)
            return student
        except:
            try:
                staff = Staff.objects.get(pk=user.pk)
                return staff
            except:
                try:
                    administrator = Administrator.objects.get(pk=user.pk)
                    return administrator
                except:
                    return user
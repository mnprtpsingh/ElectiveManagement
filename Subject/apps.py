from django.apps import AppConfig


class SubjectConfig(AppConfig):
    name = 'Subject'

    def ready(self):
        import Subject.signals
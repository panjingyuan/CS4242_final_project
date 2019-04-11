from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "mysite"
    verbose_name = "CS4242 Mini-Project Site"

    def ready(self):
        import_module("mysite.receivers")

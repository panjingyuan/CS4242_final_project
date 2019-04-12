import json
import os, sys
import django
from django.conf import settings
from django.core.management.base import BaseCommand
# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# !! https://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
import argparse
from mysite.models import Article, Category, Subcat

# TODO:
# Create a way to clear just the articles, cat and subcat
class Command(BaseCommand):
    help = 'Clears values in Article, Category and Subcat'

    #parser = argparse.ArgumentParser(description='Process some integers.')
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true')
        parser.add_argument('--art', action='store_true')
        parser.add_argument('--cat', action='store_true')
        parser.add_argument('--sub', action='store_true')

    def _confirm(self, cls, var_name):
        print("Flushing %d %s." % (cls.objects.all().count(), var_name))
        for item in cls.objects.all():
            print("-" + item)
        ans = input("Are you sure? (y) ")
        return ans == "y"

    def _clear(self, cls):
        cls.objects.all().delete()
        print("Articles flushed.")

    def handle(self, *args, **options):
        cls = []

#        print(parser.parse_args(args))
        if options["art"]:
            cls.append(Article)

        if options["cat"]:
            cls.append(Category)

        if options["sub"]:
            cls.append(Subcat)

        if options["all"]:
            cls.extend([Article, Category, Subcat])

        for class_to_delete in cls:
            if self._confirm(class_to_delete, str(class_to_delete)):
                self._clear(class_to_delete)

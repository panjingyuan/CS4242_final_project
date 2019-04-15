import json
import os, sys
import django
from django.conf import settings
from django.core.management.base import BaseCommand
# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# !! https://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
import argparse
from mysite.models import Article, Category, Subcat, Keyword

# TODO:
# Create a way to clear just the articles, cat and subcat
class Command(BaseCommand):
    help = 'Clears values in Article, Category and Subcat. Doesn\'t touch Users!'

    #parser = argparse.ArgumentParser(description='Process some integers.')
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='clear all tables')
        parser.add_argument('--art', action='store_true', help='clear all Articles')
        parser.add_argument('--cat', action='store_true', help='clear all Categories')
        parser.add_argument('--sub', action='store_true', help='clear all Subcategories')

    def _confirm(self, cls, var_name):
        print("Flushing %d %s." % (cls.objects.all().count(), var_name))
        ans = input("Are you sure? (y) ")
        return ans == "y"

    def _clear(self, cls):
        cls.objects.all().delete()
        print("%s flushed." % cls)

    def handle(self, *args, **options):
        cls = []

        if not (options["art"] or options["cat"] or options["sub"] or options["all"]):
            print("No options given, try --all --art --cat --sub")
            for item in options:
                print(item)

        if options["all"]:
            cls.extend([Category, Subcat, Article, Keyword])
        else:
            if options["art"]:
                cls.append(Article)

            if options["cat"]:
                cls.append(mysite.Category)

            if options["sub"]:
                cls.append(mysite.Subcat)


        for class_to_delete in cls:
            counts = class_to_delete.objects.all().count()
            if counts == 0:
                print("%s is empty!" % class_to_delete)
            elif self._confirm(class_to_delete, str(class_to_delete)):
                self._clear(class_to_delete)
            else:
                print("Deletion of %s cancelled." % str(class_to_delete))

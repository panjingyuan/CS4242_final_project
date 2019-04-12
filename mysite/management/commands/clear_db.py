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

    def _confirm(self, var_count, var_name):
        ans = input("Flushing %d %s. Are you sure? (y)" % (var_count, var_name))
        return ans == "y"

    def _clear(self, cls):
        cls.objects.all().delete()
        print("Articles flushed.")

    def handle(self, *args, **options):
        #fields
        DIR_NAME = "mysite/json_data/"
        OUT_DIR_NAME = "fixtures/"
        WH_FILENAME = "wikihow.json"
        IN_FILENAME = "instructables.json"
        OUT_FILENAME = "unified.json"
        APP_NAME = "mysite"
        ARTICLE_NAME = "article"

#        print(parser.parse_args(args))
        if options["art"]:
            cls = Article
            if self._confirm(cls.objects.all().count(), str(cls)):
                self._clear(cls)

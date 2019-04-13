import json
import os, sys
import django
from progress.bar import IncrementalBar
from django.conf import settings
from django.core.management.base import BaseCommand
# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# !! https://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
import argparse
from mysite.models import Article, Category, Subcat
import mysite.process as proc

# TODO:
# Create a way to read the related .json files
#
class Command(BaseCommand):
    help = 'Loads the specified json files into data.\n \
            Default: \\fixtures\\instructables.json and \
                     \\fixtures\\wikihow.json'

    #parser = argparse.ArgumentParser(description='Process some integers.')
    def add_arguments(self, parser):
        parser.add_argument('--where', action='store_true', help='returns current manage.py\'s filepath')
        parser.add_argument('--example', action='store_true', help='creates an example category')
        parser.add_argument('--store_wh', action='store_true', help='loads wikihow.json')
        parser.add_argument('--store_in', action='store_true', help='loads instructables.json')
        parser.add_argument('--store_all', action='store_true', help='loads both wikihow.json and instructables.json')

    def _get_wh_file(self, filepath):
        return proc.load_wh(filepath)

    def _get_in_file(self, filepath):
        return proc.load_in(filepath)

    def _store_wh_data(self, wh_data):
        skipped = 0
        bar = IncrementalBar('Saving records', max=len(wh_data))
        for entry in wh_data:
#            for field in proc.REQUIRED_FIELDS:
#                assert(entry[field] is not None), ("%s cannot be empty, found:\n%s" % (str(field), str(entry)))
#               wh_record[field] = entry[field]
            wh_record, created = Article.objects.get_or_create(            \
            title = entry["title"],         \
            img = entry["image"],           \
            page_url = entry["url"],        \
            views = entry["view_count"],    \
            sitetype = entry["site_type"],  \
            summary = entry["summary"],     \
            datetime = entry["date"],       \
            cat = entry["category"])
#            wh_record.cat = entry["category"]
            if not created:
                wh_record.save()
            else:
                skipped += 1
            bar.next()
        bar.finish()
        if skipped:
            print("Skipped %d duplicate entries." % skipped)

    def _make_category(self, name="Example"):
        new_cat = Category(name=name)
        new_cat.save()

    def _make_article(self):
        new_art = Article(  title="example",
                            author="example")
        new_art.save()

    def handle(self, *args, **options):
        #fields
        DIR_NAME = "mysite/json_data/"
        OUT_DIR_NAME = "fixtures/"
        WH_FILENAME = "wikihow.json"
        IN_FILENAME = "instructables.json"
        OUT_FILENAME = "unified.json"
        APP_NAME = "mysite"
        ART_NAME = "Article"
        CAT_NAME = "Category"
        SUB_NAME = "Subcat"

#        print(parser.parse_args(args))
        if options["where"]:
            print("Hello World! From manage.py!")
            print(os.getcwd())
        elif options["example"]:
            print("Making example category!")
            self._make_category()
            print("Making example article!")
            self._make_article()
        elif options["store_wh"]:
            print("Loading from " + WH_FILENAME + ": ")
            WH_data = self._get_wh_file(DIR_NAME+WH_FILENAME)
            print("%d records found for %s" % (len(WH_data),WH_FILENAME))
            self._store_wh_data(WH_data)
        elif options["store_in"]:
            print("Loading from " + IN_FILENAME + ": ")
            IN_data = self._get_in_file(DIR_NAME+IN_FILENAME)
            print("%d records found for %s" % (len(IN_data),IN_FILENAME))
